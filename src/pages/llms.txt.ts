import type { APIRoute } from "astro";
import { getAllCodes, formatCodeParams } from "../lib/queries";

export const prerender = false;

// https://llmstxt.org/ — a concise, LLM-friendly map of the site. Generated
// from the live database (like sitemap.xml) so it never drifts. Codes are the
// top-level entities; each code page enumerates its own circuits (and carries
// schema.org JSON-LD), so listing every circuit here would only add noise.
export const GET: APIRoute = ({ site }) => {
  const base = site!.origin;
  const codes = getAllCodes(); // ordered by name
  const totalCircuits = codes.reduce((sum, c) => sum + c.circuit_count, 0);

  const codeLines = codes.map((c) => {
    const params = formatCodeParams(c);
    // `includes`, not `===`: a name that already carries its parameters
    // ("[[20,2,6]] Code") would otherwise be listed as "[[20,2,6]] Code [[20,2,6]]".
    const label = params === "" || c.name.includes(params) ? c.name : `${c.name} ${params}`;
    const n = c.circuit_count;
    return `- [${label}](${base}/codes/${c.slug}): ${n} circuit${n !== 1 ? "s" : ""}`;
  });

  const body = `# QECirc

> A community-driven library for quantum error correction (QEC) circuits. Browse and download reusable STIM circuits — encoding, state preparation, syndrome extraction, and more — organized by error-correcting code. ${codes.length} codes, ${totalCircuits} circuits.

Circuits are stored in STIM format and also offered as QASM and Cirq. Each code page lists its circuits with metrics (gate count, two-qubit gate count, depth, qubit count) and links to the original source. Circuit data is licensed CC BY-SA 4.0; please cite the source of each circuit when using it.

## Codes

${codeLines.join("\n")}

## About

- [Codes](${base}/codes): browse and filter all codes by [[n,k,d]] parameters and tags.
- [About](${base}/about): project goals, data model, and scope.
- [Contribute](${base}/contribute): how to submit a circuit or import a dataset.
- [Tools](${base}/tools): software tools used to create the circuits.
- [Adding Circuits guide](https://github.com/qecirc/qecirc-website/blob/main/docs/adding-circuits.md): the ingestion pipeline and helper functions.
`;

  return new Response(body, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
};
