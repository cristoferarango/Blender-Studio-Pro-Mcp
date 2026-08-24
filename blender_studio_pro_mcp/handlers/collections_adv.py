"""Advanced collection management."""

from __future__ import annotations

import bpy


def list_collections():
    result = []
    for c in bpy.data.collections:
        result.append({
            "name": c.name,
            "objects": [o.name for o in c.objects],
            "children": [ch.name for ch in c.children],
            "hide_viewport": c.hide_viewport,
            "hide_render": c.hide_render,
        })
    return {"collections": result}


def create_collection_hierarchy(name, parent=None):
    coll = bpy.data.collections.new(name)
    if parent:
        parent_coll = bpy.data.collections.get(parent)
        if parent_coll:
            parent_coll.children.link(coll)
        else:
            bpy.context.scene.collection.children.link(coll)
            return {"name": coll.name, "warning": f"Parent '{parent}' not found; linked to scene"}
    else:
        bpy.context.scene.collection.children.link(coll)
    return {"name": coll.name, "parent": parent}


def set_collection_visibility(name, hide_viewport=None, hide_render=None):
    coll = bpy.data.collections.get(name)
    if not coll:
        return {"error": f"Collection '{name}' not found"}
    if hide_viewport is not None:
        coll.hide_viewport = hide_viewport
    if hide_render is not None:
        coll.hide_render = hide_render
    return {
        "name": name,
        "hide_viewport": coll.hide_viewport,
        "hide_render": coll.hide_render,
    }


def delete_collection(name, do_unlink_objects=False):
    coll = bpy.data.collections.get(name)
    if not coll:
        return {"error": f"Collection '{name}' not found"}
    if do_unlink_objects:
        for obj in list(coll.objects):
            coll.objects.unlink(obj)
    bpy.data.collections.remove(coll)
    return {"deleted": name}


def instance_collection(collection_name, name=None, location=(0, 0, 0)):
    coll = bpy.data.collections.get(collection_name)
    if not coll:
        return {"error": f"Collection '{collection_name}' not found"}
    instance = bpy.data.objects.new(name or f"{collection_name}_instance", None)
    instance.instance_type = "COLLECTION"
    instance.instance_collection = coll
    instance.location = location
    bpy.context.collection.objects.link(instance)
    return {"name": instance.name, "collection": collection_name}


HANDLERS = {
    "list_collections": list_collections,
    "create_collection_hierarchy": create_collection_hierarchy,
    "set_collection_visibility": set_collection_visibility,
    "delete_collection": delete_collection,
    "instance_collection": instance_collection,
}
