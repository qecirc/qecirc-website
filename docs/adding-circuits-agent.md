# Adding Circuits (Agent)

How to add circuits using the `/add-circuit` agent command in Claude Code.

For the manual workflow using Python scripts directly, see [adding-circuits.md](adding-circuits.md).

## Quick start

Run `/add-circuit` in Claude Code. The agent will walk you through the process interactively.

## What the agent does

The agent follows a 5-phase workflow:

### Phase 1: Collect inputs

The agent asks you for:

- **Required**: Hx matrix, Hz matrix, STIM circuit, code distance, source (DOI/URL)
- **Optional**: code name, Zoo URL, circuit name, tool, notes

It will not proceed without the required inputs.

### Phase 2: Inspect and validate

Before writing any files, the agent:

- Shows you the code parameters ([[n,k,d]], CSS, self-dual)
- Checks if the code already exists in the library
- Detects qubit ordering differences between your matrices and the stored code, and reports the permutation that will be applied to the circuit
- Shows circuit metrics (qubit count, gate count, depth) and a Crumble link
- Can extract Hx/Hz directly from the circuit via Pauli propagation (`extract_code`) if matrices aren't provided
- Runs validation if you tell it the circuit type (encoding or state-prep)
- Shows a dry-run preview of what files would be generated

You confirm before anything is written.

### Phase 3: Generate YAML files

The agent calls the Python API to write the code YAML, circuit YAML, and body files (`.stim`, `.qasm`, `.cirq`) to `data_yaml/`. Each circuit is automatically assigned a unique `qec_id` (displayed as `#N` in the UI). This ID is permanent and must never be reused.

### Phase 4: Zoo lookup and tagging

The agent enriches the generated YAML with tags:

- **Auto-tags** (already applied): `CSS`, `self-dual` — mathematically verified
- **Zoo lookup**: if a Zoo URL is available, the agent fetches the page and proposes tags based on the code's properties (family, structure). It only suggests tags that already exist in the library.
- **Circuit tags**: the agent asks you about functionality (`encoding`, `syndrome-extraction`, etc.) and fault tolerance (`ft`/`non-ft`). It never guesses these.
- **No optimality claims**: tags like `gate-optimal` or `depth-optimal` are only added if you or the source paper explicitly claim them.

### Phase 5: Final review

The agent shows you the final YAML files. You can request edits. Once you approve, it rebuilds the database with `npm run db:create`.

The pipeline also preserves the original (pre-canonicalization) STIM circuit and check matrices in `data_yaml/circuits/originals/`. These are viewable on the circuit detail page under "Original submission".

## What you need to provide

| Input         | Required | Notes                                             |
| ------------- | -------- | ------------------------------------------------- |
| Hx matrix     | yes      | Text, JSON, numpy-style, or file path             |
| Hz matrix     | yes      | Must have same number of columns as Hx            |
| STIM circuit  | yes      | Text, file path, or stim string                   |
| Code distance | yes      | Integer                                           |
| Source        | yes      | DOI, URL, or citation — provenance is required    |
| Code name     | no       | Agent will ask; can look up Zoo if you don't know |
| Zoo URL       | no       | Agent can search errorcorrectionzoo.org           |
| Circuit name  | no       | Agent will ask for a descriptive name             |
| Tool          | no       | e.g. `mqt-qecc`, `cliffordopt`, `flag-at-origin`  |
| Notes         | no       | Optional notes about the circuit                  |

## Tag vocabulary

The agent only uses tags that already exist in the library. Current tags:

| Level   | Tags                                                                           |
| ------- | ------------------------------------------------------------------------------ |
| Code    | `CSS`, `stabilizer`, `self-dual`, `color-code`, `concatenated`                 |
| Circuit | `encoding`, `state-preparation`, `syndrome-extraction`, `ft`, `non-ft`, `flag` |

If the Zoo or user suggests a tag not in this list, the agent will ask before adding it.
