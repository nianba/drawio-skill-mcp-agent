---
name: drawio
description: Generate polished, editable diagrams as native draw.io / diagrams.net .drawio files. Use when Codex needs to create, revise, beautify, validate, or export a diagram, flowchart, architecture diagram, ER diagram, sequence diagram, class diagram, network diagram, mockup, wireframe, UI sketch, or when the user mentions draw.io, drawio, diagrams.net, .drawio files, diagram aesthetics, or diagram export to PNG/SVG/PDF.
---

# Draw.io Diagram Skill

Create polished native `.drawio` files by writing mxGraphModel XML directly. Prefer `.drawio` as the source of truth; export to PNG, SVG, or PDF only when the user asks for a viewable artifact or visual QA needs a rendered preview.

## Workflow

1. Clarify the diagram intent only when required. For routine requests, choose a sensible layout and proceed.
2. Select the visual treatment:
   - Use the user's reference style when provided.
   - For screenshots, URLs, Figma links, mockups, or "make it look like this" requests, use the `anydesign` skill first to extract design tokens and component rules.
   - For cloud, network, Kubernetes, P&ID, electrical, or vendor-specific diagrams, prefer draw.io library shapes over generic rectangles.
   - For ordinary business/process diagrams, use a restrained professional style with clear hierarchy and generous spacing.
3. Generate uncompressed draw.io XML in mxGraphModel format.
4. Write the result to a descriptive lowercase hyphenated `.drawio` file in the working directory.
5. Validate the file:
   ```bash
   python3 <skill-dir>/scripts/validate_drawio.py path/to/file.drawio
   ```
6. If the user requested PNG, SVG, PDF, or if visual quality is important, locate the draw.io Desktop CLI and export with embedded XML.
7. For important or presentation-facing diagrams, inspect the rendered PNG/SVG/PDF visually when possible and fix overlap, clipping, cramped labels, weak contrast, or inconsistent styling before final delivery.
8. Report the absolute output path and any validation/export caveats.

## Visual Quality Rules

Use these defaults unless the user supplies a different style guide:

- Use a small palette: one primary color, one accent color, neutral fills, and semantic colors only when they communicate state.
- Keep node fills light and borders slightly darker; reserve saturated colors for key systems, decisions, or risk points.
- Use consistent typography: one font family, 12-14 px body labels, 16-18 px section titles.
- Use shape semantics: rounded rectangles for actions/services, diamonds for decisions, cylinders for data stores, swimlanes for ownership, containers for subsystems.
- Keep edges orthogonal or gently rounded; avoid unnecessary waypoints and crossing lines.
- Keep labels concise. Split dense labels across multiple nodes instead of shrinking text below readability.
- Align nodes on a grid and preserve consistent spacing between rows, columns, and containers.
- Add a title only when it helps the exported artifact stand alone.
- Prefer visual hierarchy over decoration: grouping, color roles, line weight, and whitespace should carry the design.

## Companion Skills and Tools

- Use `anydesign` before this skill when the user provides a visual reference, website, Figma file, screenshot, or asks to replicate a design language. Apply extracted colors, typography, spacing, radii, and component rules to draw.io styles.
- Use browser or Playwright-based visual inspection after export when the diagram is presentation-facing or when overlap/clipping is likely.
- Use the `pdf` skill when the requested final artifact is PDF and page rendering/layout matters.
- Use an MCP draw.io server only when live editor control, shape-library lookup, or incremental diagram mutation is more useful than direct XML generation.

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

For detailed layout, edge routing, containers, layers, metadata, and dark-mode rules, read `references/xml-reference.md`. For shape styles, palettes, labels, and style strings, read `references/style-reference.md`.

## Style Reference Loading

Keep `SKILL.md` in context for normal diagrams. Load reference files only when useful:

- `references/xml-reference.md`: layout patterns, swimlanes, containers, connectors, layers, metadata, dark-mode behavior, and XML mechanics.
- `references/style-reference.md`: shape-specific style strings, colors, typography, fills, strokes, shadows, labels, and visual polish.

When references conflict, prioritize XML validity first, then semantic clarity, then aesthetics.

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
- Poor visual quality: export a preview, inspect it, then adjust spacing, labels, contrast, grouping, and edge routing.
