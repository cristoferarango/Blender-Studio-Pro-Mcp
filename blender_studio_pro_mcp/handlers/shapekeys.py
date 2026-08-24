"""Shape keys."""

from __future__ import annotations

import bpy


def add_shape_key(object_name, name="Key", from_mix=False):
    obj = bpy.data.objects.get(object_name)
    if not obj or not getattr(obj, "data", None):
        return {"error": "Object with mesh/curve data required"}
    if obj.data.shape_keys is None:
        obj.shape_key_add(name="Basis")
    key = obj.shape_key_add(name=name, from_mix=from_mix)
    return {"object": object_name, "shape_key": key.name}


def list_shape_keys(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or not obj.data or not obj.data.shape_keys:
        return {"object": object_name, "shape_keys": []}
    keys = obj.data.shape_keys.key_blocks
    return {
        "object": object_name,
        "shape_keys": [{"name": k.name, "value": k.value, "mute": k.mute} for k in keys],
    }


def set_shape_key_value(object_name, key_name, value):
    obj = bpy.data.objects.get(object_name)
    if not obj or not obj.data.shape_keys:
        return {"error": "No shape keys"}
    key = obj.data.shape_keys.key_blocks.get(key_name)
    if not key:
        return {"error": f"Shape key '{key_name}' not found"}
    key.value = float(value)
    return {"object": object_name, "shape_key": key_name, "value": key.value}


def remove_shape_key(object_name, key_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or not obj.data.shape_keys:
        return {"error": "No shape keys"}
    key = obj.data.shape_keys.key_blocks.get(key_name)
    if not key:
        return {"error": f"Shape key '{key_name}' not found"}
    obj.shape_key_remove(key)
    return {"removed": key_name}


HANDLERS = {
    "add_shape_key": add_shape_key,
    "list_shape_keys": list_shape_keys,
    "set_shape_key_value": set_shape_key_value,
    "remove_shape_key": remove_shape_key,
}
