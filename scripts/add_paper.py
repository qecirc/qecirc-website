"""Fetch paper metadata from arXiv/Crossref and write data_yaml/papers/<slug>.yaml.

    uv run python scripts/add_paper.py 2402.17761
    uv run python scripts/add_paper.py https://arxiv.org/abs/2508.14200 10.1098/rspa.1996.0136
    uv run python scripts/add_paper.py --missing            # every unlinked circuit source
    uv run python scripts/add_paper.py --missing --dry-run  # show what it would write

WHY THIS FETCHES, WHEN NOTHING ELSE IN THE REPO DOES
----------------------------------------------------
"No external services / no third-party APIs" governs the SITE: the build
(`npm run db:create`) and every request must read only committed YAML, and they
still do. This is a maintainer tool, run once per paper, whose output is a file
you commit -- the same shape as `annotate_circuits.py`. Nothing at build or
request time depends on the network, and the site builds identically offline.

WHY IT IS NOT A HAND-WRITTEN YAML STEP
--------------------------------------
Titles and author lists are facts about real people; a wrong one is a
misattribution that then renders on the page and in schema.org JSON-LD. They are
also routinely newer than any model's training data -- two of the first seven
papers here postdate a recent cutoff -- and second-hand sources are unreliable:
one import README paraphrased its own paper's title inaccurately. So the rule is
fetch, never recall. This script exists to make the correct path the easy one.

Linking is by `source`, not by a key in circuit YAML: `create_database.mjs`
matches each circuit's `source` against every paper's url/arxiv_id/doi. So
writing the paper file IS the whole job -- no circuit is edited, and every
circuit already citing that work is enriched at the next build.

Stdlib only (urllib + xml.etree + yaml, all already present); no new dependency.
"""

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path
from xml.etree import ElementTree

import yaml

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data_yaml" / "papers"
CIRCUITS_DIR = ROOT / "data_yaml" / "circuits"

# Crossref asks for a contact so it can reach you about a misbehaving client, and
# routes politely-identified traffic to a better-served pool.
USER_AGENT = "qecirc-website (+https://github.com/qecirc/qecirc-website)"

ARXIV_API = "https://export.arxiv.org/api/query"
CROSSREF_API = "https://api.crossref.org/works"

ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

# Dropped from generated slugs -- they carry no identifying signal and only make
# the filename longer.
STOPWORDS = {
    "a", "an", "and", "for", "from", "in", "into", "of", "on", "the", "to", "with",
    "using", "via", "quantum",
}  # fmt: skip


class FetchError(Exception):
    """Metadata could not be retrieved or was too incomplete to write."""


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        raise FetchError(f"HTTP {e.code} from {url}") from e
    except Exception as e:  # URLError, timeout, SSL...
        raise FetchError(f"{type(e).__name__} from {url}: {e}") from e


def extract_ref(text: str) -> tuple[str, str] | None:
    """Reduce a source string to ("arxiv", id) or ("doi", doi), or None.

    Accepts what actually appears in `source`: an abs/pdf link, a doi.org link, or
    a bare id. Version suffixes are stripped -- v1 and v2 are the same paper, and
    the stored id is the bare one.
    """
    s = text.strip()
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([^\s?#]+?)(?:\.pdf)?(?:v\d+)?/?$", s, re.I)
    if m:
        return ("arxiv", m.group(1))
    m = re.search(r"(?:doi\.org/|^doi:)(10\.\d{4,}/\S+?)/?$", s, re.I)
    if m:
        return ("doi", m.group(1))
    if re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", s):
        return ("arxiv", re.sub(r"v\d+$", "", s))
    # Old-style arXiv id, e.g. quant-ph/9601029
    if re.fullmatch(r"[a-z-]+(\.[A-Z]{2})?/\d{7}(v\d+)?", s):
        return ("arxiv", re.sub(r"v\d+$", "", s))
    if re.fullmatch(r"10\.\d{4,}/\S+", s):
        return ("doi", s)
    return None


def fetch_arxiv(arxiv_id: str) -> dict:
    root = ElementTree.fromstring(get(f"{ARXIV_API}?id_list={arxiv_id}&max_results=1"))
    entry = root.find("a:entry", ATOM)
    # arXiv answers an unknown id with an entry whose title is "Error"; a real
    # entry always carries an <id> pointing at the abs page.
    if entry is None or entry.find("a:id", ATOM) is None:
        raise FetchError(f"arXiv returned no entry for {arxiv_id}")
    title_el = entry.find("a:title", ATOM)
    if title_el is None or not (title_el.text or "").strip():
        raise FetchError(f"arXiv entry for {arxiv_id} has no title")
    if (title_el.text or "").strip() == "Error":
        raise FetchError(f"arXiv rejected id {arxiv_id} (no such paper?)")

    authors = [
        " ".join((n.text or "").split())
        for n in entry.findall("a:author/a:name", ATOM)
        if (n.text or "").strip()
    ]
    published = entry.findtext("a:published", default="", namespaces=ATOM)

    paper = {
        # arXiv wraps long titles across lines; collapse to one.
        "title": " ".join((title_el.text or "").split()),
        "authors": authors,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "arxiv_id": arxiv_id,
    }
    if published[:4].isdigit():
        paper["year"] = int(published[:4])
    doi = entry.findtext("arxiv:doi", default="", namespaces=ATOM).strip()
    if doi:
        paper["doi"] = doi
    journal = entry.findtext("arxiv:journal_ref", default="", namespaces=ATOM).strip()
    if journal:
        paper["journal_ref"] = " ".join(journal.split())
    return paper


def fetch_crossref(doi: str) -> dict:
    msg = json.loads(get(f"{CROSSREF_API}/{doi}"))["message"]
    title = (msg.get("title") or [""])[0]
    if not title:
        raise FetchError(f"Crossref has no title for {doi}")

    authors = []
    for a in msg.get("author") or []:
        name = " ".join(x for x in (a.get("given"), a.get("family")) if x) or a.get("name") or ""
        if name:
            authors.append(name)

    paper = {"title": " ".join(title.split()), "authors": authors, "url": f"https://doi.org/{doi}",
             "doi": doi}  # fmt: skip
    for key in ("published-print", "published-online", "issued"):
        parts = (msg.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            paper["year"] = int(parts[0][0])
            break
    container = (msg.get("container-title") or [""])[0]
    if container:
        ref = container
        if msg.get("volume"):
            ref += f" {msg['volume']}"
        if msg.get("page"):
            ref += f", {msg['page']}"
        if paper.get("year"):
            ref += f" ({paper['year']})"
        paper["journal_ref"] = ref
    return paper


def fetch(kind: str, ident: str) -> dict:
    paper = fetch_arxiv(ident) if kind == "arxiv" else fetch_crossref(ident)
    # Refuse to write a paper with no authors rather than emit a half-record that
    # renders as an empty citation. Crossref genuinely lacks authors on some older
    # records (the 1996 Steane paper among them) -- for those, pass the arXiv id
    # instead, which has them. Guessing the names here is not an option.
    if not paper["authors"]:
        raise FetchError(
            f"no authors in {kind} metadata for {ident} -- "
            f"if this work has an arXiv preprint, pass its id instead"
        )
    return paper


def surname(full_name: str) -> str:
    return full_name.strip().split()[-1] if full_name.strip() else ""


def ascii_fold(text: str) -> str:
    """Latin text to its ASCII skeleton, for slugs only.

    Dropping non-ASCII instead of folding it silently mangles exactly the names
    this catalogue is full of: "Brugière" -> "brugire", "Müller" -> "mller".
    NFKD splits a letter from its accent so the accent can be dropped and the
    letter kept -- but it does NOT decompose ligature-like letters, so "Heußen"
    would become "heuen". Those are mapped first, by hand.
    """
    for src, dst in (("ß", "ss"), ("æ", "ae"), ("œ", "oe"), ("ø", "o"), ("đ", "d"), ("ł", "l")):
        text = text.replace(src, dst).replace(src.upper(), dst.upper())
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def slugify(paper: dict) -> str:
    """<first-author>-<year>-<a few title words>, matching the existing files."""
    parts = [re.sub(r"[^a-z0-9]+", "", ascii_fold(surname(paper["authors"][0])).lower())]
    if paper.get("year"):
        parts.append(str(paper["year"]))
    title = ascii_fold(paper["title"]).lower()
    words = [w for w in re.findall(r"[a-z0-9]+", title) if w not in STOPWORDS]
    parts.extend(words[:4])
    return "-".join(p for p in parts if p)


def existing_refs() -> dict[tuple[str, str], str]:
    """Every (kind, id) the library already holds -> the file holding it.

    Keyed on the identifiers rather than on URL shape: an arXiv id is an arXiv id
    however it is written, so this needs none of the URL normalization that
    scripts/paper-links.mjs does at build time. That normalizer stays the single
    authority on whether a `source` actually links -- and `db:create` reports any
    that does not, which is the backstop if these two ever disagree.
    """
    refs: dict[tuple[str, str], str] = {}
    for path in sorted(PAPERS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        if data.get("arxiv_id"):
            refs[("arxiv", str(data["arxiv_id"]))] = path.name
        if data.get("doi"):
            refs[("doi", str(data["doi"]))] = path.name
        ref = extract_ref(str(data.get("url", "")))
        if ref:
            refs[ref] = path.name
    return refs


def circuit_sources() -> dict[str, int]:
    """Every link-shaped `source` in circuit YAML -> how many circuits use it."""
    counts: dict[str, int] = {}
    for path in sorted(CIRCUITS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        source = str(data.get("source", ""))
        # A non-link source names a tool ("circuit-synth"), which is provenance
        # but not a paper.
        if source.startswith(("http://", "https://")):
            counts[source] = counts.get(source, 0) + 1
    return counts


def write_paper(paper: dict, dry_run: bool) -> Path:
    slug = slugify(paper)
    path = PAPERS_DIR / f"{slug}.yaml"
    # Field order mirrors the hand-written files.
    ordered = {k: paper[k] for k in
               ("title", "authors", "year", "arxiv_id", "doi", "journal_ref", "url")
               if k in paper}  # fmt: skip
    text = yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True, width=1000)
    # `arxiv_id: 2402.17761` unquoted is a YAML FLOAT and an id ending in 0 loses
    # it. safe_dump quotes it because it is a str -- assert that rather than trust
    # it, since the failure is silent and validate:yaml would only catch it later.
    if "arxiv_id" in ordered:
        assert re.search(r"arxiv_id: ['\"]", text), f"arxiv_id must be quoted, got:\n{text}"
    if not dry_run:
        path.write_text(text)
    return path


def add(ref_text: str, existing: dict[tuple[str, str], str], dry_run: bool) -> str:
    ref = extract_ref(ref_text)
    if ref is None:
        return f"SKIP  {ref_text}\n      not an arXiv or DOI reference — add this paper by hand"
    if ref in existing:
        return f"HAVE  {ref[1]} — already in papers/{existing[ref]}"

    paper = fetch(*ref)
    path = write_paper(paper, dry_run)
    # Register both identities so a --missing run cannot fetch the same work twice
    # under its arXiv id and its DOI.
    existing[ref] = path.name
    if paper.get("arxiv_id"):
        existing[("arxiv", paper["arxiv_id"])] = path.name
    if paper.get("doi"):
        existing[("doi", paper["doi"])] = path.name

    verb = "WOULD" if dry_run else "WROTE"
    authors = paper["authors"]
    credit = authors[0] if len(authors) == 1 else f"{surname(authors[0])} et al."
    year = paper.get("year", "?")
    return f"{verb} papers/{path.name}\n      {credit} ({year}) — {paper['title']}"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Fetch paper metadata into data_yaml/papers/.",
        epilog="Run `npm run db:create` afterwards to link circuits to the new papers.",
    )
    ap.add_argument("refs", nargs="*", help="arXiv id, DOI, or link (abs/pdf/doi.org)")
    ap.add_argument(
        "--missing",
        action="store_true",
        help="add every circuit `source` that has no paper yet",
    )
    ap.add_argument("--dry-run", action="store_true", help="report without writing")
    args = ap.parse_args()

    if not args.refs and not args.missing:
        ap.error("give at least one reference, or --missing")

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    existing = existing_refs()
    refs = list(args.refs)

    if args.missing:
        for source, count in sorted(circuit_sources().items(), key=lambda kv: -kv[1]):
            ref = extract_ref(source)
            if ref is None:
                print(f"SKIP  {source} ({count} circuits)\n      not arXiv/DOI — add by hand")
                continue
            if ref in existing:
                continue
            refs.append(source)
        if not refs:
            print("Nothing missing: every circuit source already has a paper.")
            return 0

    failed = 0
    for ref_text in refs:
        try:
            print(add(ref_text, existing, args.dry_run))
        except FetchError as e:
            print(f"FAIL  {ref_text}\n      {e}", file=sys.stderr)
            failed += 1

    if not args.dry_run and failed == 0:
        print("\nNow run: npm run db:create")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
