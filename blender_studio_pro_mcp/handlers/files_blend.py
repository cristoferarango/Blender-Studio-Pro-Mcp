"""Blend file operations: save, open, append, link, new."""

from __future__ import annotations

import bpy


def get_filepath():
    return {
        "filepath": bpy.data.filepath,
        "is_saved": bool(bpy.data.filepath),
        "is_dirty": bpy.data.is_dirty,
    }


def save_blend(filepath=None):
    if filepath:
        bpy.ops.wm.save_as_mainfile(filepath=filepath)
    else:
        if not bpy.data.filepath:
            return {"error": "No filepath set; pass filepath=..."}
        bpy.ops.wm.save_mainfile()
    return get_filepath()


def open_blend(filepath):
    bpy.ops.wm.open_mainfile(filepath=filepath)
    return get_filepath()


def new_blend(reset_ui=False):
    bpy.ops.wm.read_homefile(use_empty=True)
    return {"status": "ok", "new_file": True}


def append_from_blend(filepath, directory, filename):
    """Append a datablock. directory e.g. 'Object/', filename e.g. 'Cube'."""
    bpy.ops.wm.append(
        filepath=filepath,
        directory=f"{filepath}/{directory}",
        filename=filename,
    )
    return {"appended": filename, "from": filepath, "directory": directory}


def link_from_blend(filepath, directory, filename):
    bpy.ops.wm.link(
        filepath=filepath,
        directory=f"{filepath}/{directory}",
        filename=filename,
    )
    return {"linked": filename, "from": filepath, "directory": directory}


def pack_resources():
    bpy.ops.file.pack_all()
    return {"status": "ok", "action": "pack_all"}


def unpack_resources(method="USE_LOCAL"):
    bpy.ops.file.unpack_all(method=method)
    return {"status": "ok", "method": method}


HANDLERS = {
    "get_filepath": get_filepath,
    "save_blend": save_blend,
    "open_blend": open_blend,
    "new_blend": new_blend,
    "append_from_blend": append_from_blend,
    "link_from_blend": link_from_blend,
    "pack_resources": pack_resources,
    "unpack_resources": unpack_resources,
}
