---
name: drawio
description: Generate editable diagrams as native draw.io / diagrams.net .drawio files. Use when Codex needs to create, revise, validate, or export a diagram, flowchart, architecture diagram, ER diagram, sequence diagram, class diagram, network diagram, mockup, wireframe, UI sketch, or when the user mentions draw.io, drawio, diagrams.net, .drawio files, or diagram export to PNG/SVG/PDF.
---

# Draw.io Diagram Skill

Create native `.drawio` files by writing mxGraphModel XML directly. Prefer `.drawio` as the source of truth; export to PNG, SVG, or PDF only when the user asks for a viewable artifact.

## Workflow

1. Clarify the diagram intent only when required. For routine requests, choose a sensible layout and proceed.
2. Generate uncompressed draw.io XML in mxGraphModel format.
3. Write the result to a descriptive lowercase hyphenated `.drawio` file in the working directory.
4. Validate the file:
   ```bash
   python3 <skill-dir>/scripts/validate_drawio.py path/to/file.drawio
   ```
5. If the user requested PNG, SVG, or PDF, locate the draw.io Desktop CLI and export with embedded XML.
6. Report the absolute output path and any validation/export caveats.

## XML Requirements

Every diagram must include the root cells:

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
  </root>
</mxGraphModel>
```

Rules:

- Do not generate compressed draw.io payloads.
- Do not include XML comments.
- Escape attribute values: `&amp;`, `&lt;`, `&gt;`, `&quot;`.
- Use unique `id` values for every `mxCell`.
- Put ordinary cells under `parent="1"` unless deliberately using layers.
- Use `vertex="1"` for nodes and include `<mxGeometry ... as="geometry"/>`.
- Use `edge="1"` for connectors, set valid `source` and `target` ids, and include `<mxGeometry relative="1" as="geometry"/>`.
- Keep labels short enough to fit inside their shapes.

For detailed style, layout, edge routing, containers, layers, metadata, and dark-mode rules, read `references/xml-reference.md`.

## Exporting

Supported export formats:

| Format | Embedded XML | Extension |
| --- | --- | --- |
| PNG | yes | `.drawio.png` |
| SVG | yes | `.drawio.svg` |
| PDF | yes | `.drawio.pdf` |
| JPG | no | `.jpg` |

Locate draw.io Desktop CLI:

```bash
# macOS
/Applications/draw.io.app/Contents/MacOS/draw.io

# Linux
drawio

# Windows
C:\Program Files\draw.io\draw.io.exe
```

Export command:

```bash
drawio -x -f <png|svg|pdf|jpg> -e -b 10 -o output.drawio.png input.drawio
```

Use `-e` / `--embed-diagram` for PNG, SVG, and PDF. After a successful embedded export, the intermediate `.drawio` may be deleted only if the exported file is the requested final source.

## Troubleshooting

- CLI missing: keep the `.drawio` file and tell the user to open it in diagrams.net or install draw.io Desktop.
- Blank diagram: verify cells `id="0"` and `id="1"` exist and visible nodes have geometry.
- Missing edges: verify every edge has valid `source`, `target`, and child geometry.
- XML parse failure: run the validation script and remove comments or unescaped characters.
