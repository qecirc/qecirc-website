"""
CLI: Insert a reviewed YAML payload into the SQLite database.

Usage:
    python -m scripts.add_circuit.insert payload.yaml
"""

import argparse
import json
import sqlite3
import sys

import yaml


DB_PATH = "data/qecirc.db"


def main():
    parser = argparse.ArgumentParser(description="Insert YAML payload into DB")
    parser.add_argument("yaml_file", help="Path to YAML payload")
    parser.add_argument("--db", default=DB_PATH, help="Path to SQLite DB")
    args = parser.parse_args()

    with open(args.yaml_file) as f:
        payload = yaml.safe_load(f)

    conn = sqlite3.connect(args.db)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        with conn:
            code_id = _insert_code(conn, payload["code"])
            for circ in payload.get("circuits", []):
                _insert_circuit(conn, circ, code_id)
        print("Insert complete.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()


def _insert_code(conn, code):
    """Insert or return existing code."""
    if code["status"] == "existing":
        print(f"Code already exists: id={code['id']}")
        return code["id"]

    cur = conn.execute(
        """INSERT INTO codes (name, slug, n, k, d, zoo_url, hx, hz, logical_x, logical_z, canonical_hash)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            code["name"], code["slug"], code["n"], code["k"], code["d"],
            code.get("zoo_url"),
            json.dumps(code["hx"]), json.dumps(code["hz"]),
            json.dumps(code["logical_x"]), json.dumps(code["logical_z"]),
            code.get("canonical_hash"),
        ),
    )
    code_id = cur.lastrowid
    print(f"Inserted code: {code['name']} (id={code_id})")

    for tag in code.get("tags", []):
        _add_tag(conn, tag["name"], code_id, "code")

    return code_id


def _insert_circuit(conn, circ, code_id):
    """Insert a circuit + bodies + tags."""
    # Resolve tool
    tool_id = None
    if circ.get("tool"):
        row = conn.execute("SELECT id FROM tools WHERE slug = ?", (circ["tool"],)).fetchone()
        if row:
            tool_id = row[0]
        else:
            print(f"  Warning: tool '{circ['tool']}' not found in DB")

    cur = conn.execute(
        """INSERT INTO circuits (code_id, name, slug, description, source,
           gate_count, depth, qubit_count, crumble_url, quirk_url, tool_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            code_id, circ["name"], circ["slug"], circ.get("description", ""),
            circ.get("source", ""),
            circ.get("gate_count"), circ.get("depth"), circ.get("qubit_count"),
            circ.get("crumble_url"), circ.get("quirk_url"),
            tool_id,
        ),
    )
    circuit_id = cur.lastrowid
    print(f"  Inserted circuit: {circ['name']} (id={circuit_id})")

    for body in circ.get("bodies", []):
        if body.get("body"):
            conn.execute(
                "INSERT INTO circuit_bodies (circuit_id, format, body) VALUES (?, ?, ?)",
                (circuit_id, body["format"], body["body"]),
            )

    for tag in circ.get("tags", []):
        _add_tag(conn, tag["name"], circuit_id, "circuit")


def _add_tag(conn, tag_name, taggable_id, taggable_type):
    conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag_name,))
    row = conn.execute("SELECT id FROM tags WHERE name = ?", (tag_name,)).fetchone()
    conn.execute(
        "INSERT OR IGNORE INTO taggings (tag_id, taggable_id, taggable_type) VALUES (?, ?, ?)",
        (row[0], taggable_id, taggable_type),
    )


if __name__ == "__main__":
    main()
