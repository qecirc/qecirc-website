/** The "please cite" toast raised after copying or downloading a circuit body.
 *
 * Shared by CodeBlock.astro (circuit detail pages) and circuit-bodies-client.ts
 * (the switchers built client-side on code pages). It lived in both before,
 * which is exactly the kind of pair that drifts.
 *
 * `citation` is the human-readable label for the link — "Zen et al. (2024),
 * <title>" — set wherever the circuit's source resolved to a paper. Without one
 * the URL is its own label, which is all a bare source can offer.
 */
export function citeNotice(source: string, citation?: string): void {
  if (typeof window.showCiteToast !== "function") return;

  const msg = "Please cite the source when using this circuit:";
  if (source && source.startsWith("http")) {
    window.showCiteToast(msg, source, citation);
  } else if (source) {
    // A non-link source names a tool, so there is nothing to link to.
    window.showCiteToast(`${msg} ${citation || source}`);
  } else {
    window.showCiteToast("Please check and cite the corresponding source when using this circuit.");
  }
}
