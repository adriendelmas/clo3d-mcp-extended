"""File exchange and CLO's asset library."""

from clo3d_mcp.server import _send, mcp


@mcp.tool()
def export_pattern_json(file_path: str) -> dict:
    """Export the pattern pieces of the project to a JSON file (absolute path)."""
    return _send("export_pattern_json", {"file_path": file_path})


@mcp.tool()
def import_pattern_json(file_path: str) -> dict:
    """Load pattern pieces from a CLO3D pattern JSON file (absolute path).

    WARNING: this REPLACES the whole scene with the pieces of the file. Save the project first.
    Graphics (logos) are not stored in this JSON and are lost. Use it to build a new garment in one go:
    pieces, seams (SeamLinePairGroupList), notches (NotchList), buttons (ButtonHeadList) and buttonholes
    (ButtonHoleList), in the coordinates of the 2D window, as written by export_pattern_json.
    """
    return _send("import_pattern_json", {"file_path": file_path})


@mcp.tool()
def export_pom() -> dict:
    """Export the points of measure of the garment. Returns the file path in CLO's temporary folder."""
    return _send("export_pom")


@mcp.tool()
def export_garment_information(file_path: str | None = None) -> dict:
    """Save the garment information sheet to JSON. Without a path, it goes to CLO's temporary folder."""
    return _send("export_garment_information", {"file_path": file_path})


@mcp.tool()
def import_garment_information(file_path: str) -> dict:
    """Load a garment information sheet from JSON (absolute path)."""
    return _send("import_garment_information", {"file_path": file_path})


@mcp.tool()
def export_bom(file_path: str) -> dict:
    """Save the bill of materials: fabrics, trims and quantities (absolute path)."""
    return _send("export_bom", {"file_path": file_path})


@mcp.tool()
def export_zpac(file_path: str) -> dict:
    """Save the garment as a .zpac package (absolute path)."""
    return _send("export_zpac", {"file_path": file_path})


@mcp.tool()
def get_clo_folders() -> dict:
    """Get CLO's asset library, temporary and executable folders."""
    return _send("get_clo_folders")


@mcp.tool()
def find_assets(extensions: list[str], root: str | None = None, limit: int = 100) -> dict:
    """List files of CLO's asset library by extension, for example ["avt"] for avatars, ["zfab"] for fabrics."""
    return _send("find_assets", {"extensions": extensions, "root": root, "limit": limit})

