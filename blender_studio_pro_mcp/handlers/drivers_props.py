"""Drivers and custom properties."""

from __future__ import annotations

import bpy


def add_driver(object_name, data_path, index=-1, expression="var"):
    """Add a driver to an object property. data_path e.g. 'location'."""
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    try:
        fcurve = obj.driver_add(data_path, index)
    except Exception as e:
        return {"error": str(e)}
    drivers = fcurve if isinstance(fcurve, list) else [fcurve]
    for fc in drivers:
        drv = fc.driver
        drv.type = "SCRIPTED"
        drv.expression = expression
    return {
        "object": object_name,
        "data_path": data_path,
        "index": index,
        "expression": expression,
    }


def remove_driver(object_name, data_path, index=-1):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    try:
        obj.driver_remove(data_path, index)
        return {"removed": f"{object_name}.{data_path}"}
    except Exception as e:
        return {"error": str(e)}


def set_custom_property(object_name, prop_name, value):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    obj[prop_name] = value
    return {"object": object_name, "property": prop_name, "value": value}


def get_custom_properties(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    props = {k: obj[k] for k in obj.keys() if not k.startswith("_")}
    return {"object": object_name, "properties": props}


def delete_custom_property(object_name, prop_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    if prop_name in obj:
        del obj[prop_name]
        return {"deleted": prop_name}
    return {"error": f"Property '{prop_name}' not found"}


HANDLERS = {
    "add_driver": add_driver,
    "remove_driver": remove_driver,
    "set_custom_property": set_custom_property,
    "get_custom_properties": get_custom_properties,
    "delete_custom_property": delete_custom_property,
}
