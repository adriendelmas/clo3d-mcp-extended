# clo3d-mcp-extended

Drive CLO3D from an AI assistant (Claude, Cursor, opencode or any MCP client): create pattern pieces, sew
them, place them on the avatar, set fabrics and their materials, add sewn patches with logos, topstitches,
gathers and elastics, simulate, and look at the result.

Derived from [clo3d-mcp](https://github.com/Ubani-Studio/clo3d-mcp) by Violet Sphinx, with a working plugin
listener and **170 tools** instead of 33. Tested live on **CLO3D 2025.2.236, Windows 11**.

## What changed from the original

- **The plugin actually listens.** CLO3D's embedded Python freezes background threads once a Script Editor run
  returns, so the original plugin never answered. Here it polls through a native Windows timer driven by
  CLO3D's own event loop: CLO3D stays fully usable while the plugin listens. Other platforms fall back to a
  blocking loop (untested on macOS).
- **The server starts.** `mcp` is pinned below 2, and `FastMCP(instructions=...)` replaces an argument that
  no 1.x release accepts.
- **137 new tools**, each an explicit, typed plug-in command. No generic "call any function" entry point.
- **Fixes** for API calls that raised errors on current CLO builds (`GetFabricCount`, `SetSimulationQuality`,
  `CopyColorway`) and a handler for `replace_fabric`, which had none.

See [docs/TOOLS.md](docs/TOOLS.md) for every tool.

| Area | Tools | Examples |
|---|---|---|
| Original | 33 | patterns, fabrics, export, import, simulation, colorways |
| Geometry | 24 | internal shapes, annotations, instances, symmetry, unfold, selection |
| Sewing | 14 | sew outline or internal lines, topstitches and their styles, seam tape, shirring, elastic |
| Simulation | 15 | avatar arrangement, layers, stiffness, shrinkage, mesh, advanced settings |
| Materials | 39 | fabric textures and PBR settings, fabric duplication, graphics, trims, buttons, zippers |
| Avatar | 16 | avatars, measurements CSV, poses, CLO's own grading sizes |
| Files | 9 | pattern JSON, garment information, bill of materials, CLO asset library |
| Visuals | 13 | camera, view images, 2D pattern snapshot, stress and strain maps, technical drawing |
| Nesting | 4 | automatic layout on the fabric width |
| Docs | 3 | list and describe the CLO Python API, read-only |

## Install

Requires CLO3D with Python scripting, Python 3.10 or newer, and an MCP client.

```
git clone https://github.com/adriendelmas/clo3d-mcp-extended.git
cd clo3d-mcp-extended
python -m venv .venv
.venv\Scripts\python -m pip install -e .
```

Register the server, for example with Claude Code:

```
claude mcp add --scope user clo3d -- <absolute path>\.venv\Scripts\clo3d-mcp.exe
```

## Load the plugin in CLO3D

1. **Script > Script Editor**, open `plugin/clo3d_mcp_plugin.py`, click **Run**. Once per CLO3D session.
2. The console shows `[CLO MCP] Listening for commands in: ...` and `CLO3D stays usable while listening.`
3. Re-running the script replaces the previous listener. After editing the plugin, reopen the file from disk:
   the Script Editor keeps the old text in memory.

The server and the plugin talk through JSON files in `%TEMP%\clo3d_mcp` (override with `CLO3D_MCP_DIR`).

## Known limits (CLO3D 2025.2)

- **Option classes are not exposed to Python** (`ImportExportOption`, `ImportZPRJOption`, `ImportDxfOption`,
  `CloApiRgb`). Functions that need them are left out: opening a project without dialog, DXF import with
  options, measurements with a given avatar, auto-hang, setting colorway colors.
- **Placing a logo directly** (`add_graphic_to_pattern`) works on pieces drawn in CLO, was refused on pieces
  created by script, and lands only approximately. Placed graphics cannot be moved or deleted through the
  API. For exact logos, use a **sewn patch**: a piece whose fabric texture is the logo (`duplicate_fabric`,
  `set_fabric_maps`), sewn on an internal shape drawn at the right place (`create_internal_shape`,
  `sew_lines` with `child_b`).
- **`import_pattern_json` replaces the whole scene.** Use it to build a garment in one go: pieces, seams,
  notches (`NotchList`), buttons (`ButtonHeadList`) and buttonholes (`ButtonHoleList`), in the coordinates
  written by `export_pattern_json`. Graphics are not stored in that JSON.
- **Avatar tools** fail with a clear error when no avatar is loaded, instead of CLO's blocking dialog.
- `ExportDXF` opens a dialog and is not exposed. `MovePatternPoint` broke pieces in tests and is not exposed.

## Development

```
python tests/check_static.py          # no CLO3D needed: syntax, ASCII plugin, every tool wired to a command
.venv\Scripts\python -m pip install -e .[dev]
.venv\Scripts\python -m pytest tests  # mock plug-in, no CLO3D needed
```

- `plugin/clo3d_mcp_plugin.py` is a single file, as CLO3D's Script Editor loads it. Additions live in
  `EXTENDED` sections. Keep it ASCII.
- Original tools stay in `src/clo3d_mcp/server.py`; new tools live in `src/clo3d_mcp/extended/`, one module
  per area. A tool name matches its plug-in command.

## Credits and licence

MIT, see [LICENSE](LICENSE) and [NOTICE](NOTICE). Original work by Violet Sphinx (Ubani-Studio). CLO3D is a
trademark of CLO Virtual Fashion Inc.; this project is not affiliated with or endorsed by it. CLO's SDK
headers shipped by the original repository are not included here.
