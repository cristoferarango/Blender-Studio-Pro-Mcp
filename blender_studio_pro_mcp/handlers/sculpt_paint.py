"""Sculpt and paint mode helpers."""

from __future__ import annotations

import bpy


def enter_sculpt_mode(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="SCULPT")
    return {"object": object_name, "mode": "SCULPT"}


def set_sculpt_brush(brush_name=None, size=None, strength=None):
    """Configure active sculpt brush."""
    tool = bpy.context.tool_settings.sculpt
    brush = tool.brush
    if brush_name:
        found = bpy.data.brushes.get(brush_name)
        if found:
            tool.brush = found
            brush = found
        else:
            return {"error": f"Brush '{brush_name}' not found"}
    if size is not None and brush:
        brush.size = int(size)
    if strength is not None and brush:
        brush.strength = float(strength)
    return {
        "brush": brush.name if brush else None,
        "size": brush.size if brush else None,
        "strength": brush.strength if brush else None,
    }


def list_brushes(mode="sculpt"):
    """List brushes. mode hint only; returns all brush names with use flags."""
    brushes = []
    for b in bpy.data.brushes:
        brushes.append({
            "name": b.name,
            "use_paint_sculpt": getattr(b, "use_paint_sculpt", False),
            "use_paint_vertex": getattr(b, "use_paint_vertex", False),
            "use_paint_weight": getattr(b, "use_paint_weight", False),
            "use_paint_image": getattr(b, "use_paint_image", False),
        })
    return {"brushes": brushes, "count": len(brushes)}


def enter_vertex_paint(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="VERTEX_PAINT")
    return {"object": object_name, "mode": "VERTEX_PAINT"}


def enter_weight_paint(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
    return {"object": object_name, "mode": "WEIGHT_PAINT"}


def enter_texture_paint(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="TEXTURE_PAINT")
    return {"object": object_name, "mode": "TEXTURE_PAINT"}


def remesh(object_name, mode="VOXEL", voxel_size=0.1):
    """Remesh mesh. mode: VOXEL, SMOOTH, SHARP, BLOCKS."""
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    bpy.context.view_layer.objects.active = obj
    mesh = obj.data
    mesh.remesh_mode = mode if mode in {"VOXEL", "SMOOTH", "SHARP", "BLOCKS"} else "VOXEL"
    if hasattr(mesh, "remesh_voxel_size"):
        mesh.remesh_voxel_size = voxel_size
    bpy.ops.object.mode_set(mode="OBJECT")
    try:
        bpy.ops.object.voxel_remesh()
    except Exception:
        bpy.ops.object.remesh()
    return {"object": object_name, "mode": mode, "voxel_size": voxel_size}


HANDLERS = {
    "enter_sculpt_mode": enter_sculpt_mode,
    "set_sculpt_brush": set_sculpt_brush,
    "list_brushes": list_brushes,
    "enter_vertex_paint": enter_vertex_paint,
    "enter_weight_paint": enter_weight_paint,
    "enter_texture_paint": enter_texture_paint,
    "remesh": remesh,
}
