"""Curves, text, and fonts."""

from __future__ import annotations

import bpy


def create_curve(type="BEZIER", name=None, location=(0, 0, 0)):
    """type: BEZIER, NURBS, PATH"""
    if type == "PATH":
        bpy.ops.curve.primitive_nurbs_path_add(location=location)
    elif type == "NURBS":
        bpy.ops.curve.primitive_nurbs_curve_add(location=location)
    else:
        bpy.ops.curve.primitive_bezier_curve_add(location=location)
    obj = bpy.context.active_object
    if name:
        obj.name = name
    return {"name": obj.name, "type": type}


def create_text(body="Text", name=None, location=(0, 0, 0), size=1.0, extrude=0.0):
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.active_object
    if name:
        obj.name = name
    obj.data.body = body
    obj.data.size = size
    obj.data.extrude = extrude
    return {"name": obj.name, "body": body, "size": size}


def set_text_body(object_name, body):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "FONT":
        return {"error": "Text (FONT) object required"}
    obj.data.body = body
    return {"name": object_name, "body": body}


def set_curve_geometry(object_name, bevel_depth=None, extrude=None, resolution_u=None, bevel_resolution=None):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type not in {"CURVE", "FONT"}:
        return {"error": "Curve or text object required"}
    data = obj.data
    applied = {}
    if bevel_depth is not None:
        data.bevel_depth = bevel_depth
        applied["bevel_depth"] = bevel_depth
    if extrude is not None:
        data.extrude = extrude
        applied["extrude"] = extrude
    if resolution_u is not None:
        data.resolution_u = resolution_u
        applied["resolution_u"] = resolution_u
    if bevel_resolution is not None:
        data.bevel_resolution = bevel_resolution
        applied["bevel_resolution"] = bevel_resolution
    return {"object": object_name, "applied": applied}


def convert_to_mesh(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target="MESH")
    return {"name": bpy.context.active_object.name, "type": "MESH"}


HANDLERS = {
    "create_curve": create_curve,
    "create_text": create_text,
    "set_text_body": set_text_body,
    "set_curve_geometry": set_curve_geometry,
    "convert_to_mesh": convert_to_mesh,
}
