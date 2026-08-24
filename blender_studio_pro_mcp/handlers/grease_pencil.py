"""Grease Pencil / 2D animation tools."""

from __future__ import annotations

import bpy


def create_grease_pencil(name="GPencil", location=(0, 0, 0)):
    """Create a grease pencil object (Blender 4+/5 compatible)."""
    try:
        gp_data = bpy.data.grease_pencils_v3.new(name) if hasattr(bpy.data, "grease_pencils_v3") else None
    except Exception:
        gp_data = None
    if gp_data is None:
        # Legacy / fallback
        if hasattr(bpy.data, "grease_pencils"):
            gp_data = bpy.data.grease_pencils.new(name)
        else:
            bpy.ops.object.gpencil_add(type="EMPTY", location=location)
            obj = bpy.context.active_object
            if name:
                obj.name = name
            return {"name": obj.name, "type": "GPENCIL"}
    obj = bpy.data.objects.new(name, gp_data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    bpy.context.view_layer.objects.active = obj
    return {"name": obj.name, "type": obj.type}


def add_gp_layer(object_name, layer_name="Layer"):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    data = obj.data
    if hasattr(data, "layers"):
        layer = data.layers.new(layer_name)
        return {"object": object_name, "layer": layer.name}
    return {"error": "Object has no grease pencil layers", "hint": "Use call_operator with greasepencil/gpencil ops"}


def list_gp_layers(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    data = obj.data
    if not hasattr(data, "layers"):
        return {"error": "No layers attribute"}
    return {
        "object": object_name,
        "layers": [getattr(l, "name", str(l)) for l in data.layers],
    }


def set_gp_stroke_settings(object_name, color=(0, 0, 0, 1), strength=1.0):
    """Best-effort material/color setup for GP."""
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    mat = bpy.data.materials.new(name=f"{object_name}_GPMat")
    if hasattr(mat, "is_grease_pencil"):
        try:
            bpy.data.materials.create_gpencil_data(mat)
        except Exception:
            pass
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return {"object": object_name, "material": mat.name, "color": list(color), "strength": strength}


HANDLERS = {
    "create_grease_pencil": create_grease_pencil,
    "add_gp_layer": add_gp_layer,
    "list_gp_layers": list_gp_layers,
    "set_gp_stroke_settings": set_gp_stroke_settings,
}
