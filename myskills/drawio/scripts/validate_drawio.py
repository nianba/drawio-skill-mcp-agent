#!/usr/bin/env python3
"""Validate basic structural requirements for native .drawio XML files."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def fail(message: str) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a .drawio mxGraphModel file.")
    parser.add_argument("file", type=Path, help="Path to a .drawio file")
    args = parser.parse_args()

    path = args.file
    if not path.exists():
        fail(f"File does not exist: {path}")
    if path.suffix != ".drawio":
        fail(f"Expected a .drawio file, got: {path.name}")

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        fail(f"XML parse error: {exc}")

    root = tree.getroot()
    if root.tag != "mxGraphModel":
        fail(f"Root element must be mxGraphModel, got: {root.tag}")

    graph_root = root.find("root")
    if graph_root is None:
        fail("Missing <root> element")

    cells = graph_root.findall("mxCell")
    ids: dict[str, ET.Element] = {}
    for cell in cells:
        cell_id = cell.get("id")
        if not cell_id:
            fail("Found mxCell without id")
        if cell_id in ids:
            fail(f"Duplicate mxCell id: {cell_id}")
        ids[cell_id] = cell

    if "0" not in ids:
        fail('Missing root mxCell id="0"')
    if ids.get("1") is None or ids["1"].get("parent") != "0":
        fail('Missing default parent mxCell id="1" parent="0"')

    for cell_id, cell in ids.items():
        if cell.get("vertex") == "1" and cell.find("mxGeometry") is None:
            fail(f"Vertex cell {cell_id} is missing mxGeometry")
        if cell.get("edge") == "1":
            source = cell.get("source")
            target = cell.get("target")
            if source not in ids:
                fail(f"Edge {cell_id} references missing source: {source}")
            if target not in ids:
                fail(f"Edge {cell_id} references missing target: {target}")
            geometry = cell.find("mxGeometry")
            if geometry is None or geometry.get("relative") != "1":
                fail(f"Edge {cell_id} must include mxGeometry relative=\"1\"")

    print(f"[OK] Valid draw.io XML: {path}")


if __name__ == "__main__":
    main()
