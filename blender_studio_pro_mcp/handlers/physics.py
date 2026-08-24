"""Physics: rigid body, cloth, soft body, fluid, collision."""

from __future__ import annotations

import bpy


def add_rigid_body(object_name, type="ACTIVE", mass=1.0):
    """Add rigid body physics. type: ACTIVE or PASSIVE."""
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    if not obj.rigid_body:
        bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = type
    obj.rigid_body.mass = mass
    return {"object": object_name, "type": type, "mass": mass}


def remove_rigid_body(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    bpy.context.view_layer.objects.active = obj
    if obj.rigid_body:
        bpy.ops.rigidbody.object_remove()
    return {"removed": object_name}


def add_cloth(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    mod = obj.modifiers.new(name="Cloth", type="CLOTH")
    return {"object": object_name, "modifier": mod.name}


def add_soft_body(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    mod = obj.modifiers.new(name="Softbody", type="SOFT_BODY")
    return {"object": object_name, "modifier": mod.name}


def add_collision(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    mod = obj.modifiers.new(name="Collision", type="COLLISION")
    return {"object": object_name, "modifier": mod.name}


def add_fluid_domain(object_name, domain_type="LIQUID"):
    """domain_type: GAS, LIQUID."""
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    mod = obj.modifiers.new(name="Fluid", type="FLUID")
    mod.fluid_type = "DOMAIN"
    mod.domain_settings.domain_type = domain_type
    return {"object": object_name, "domain_type": domain_type}


def add_fluid_flow(object_name, flow_type="SMOKE"):
    """flow_type: SMOKE, FIRE, LIQUID, etc."""
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    mod = obj.modifiers.new(name="Fluid", type="FLUID")
    mod.fluid_type = "FLOW"
    try:
        mod.flow_settings.flow_type = flow_type
    except Exception:
        pass
    return {"object": object_name, "flow_type": flow_type}


def bake_physics(object_name=None):
    """Bake rigid body / point cache where possible."""
    try:
        bpy.ops.ptcache.bake_all(bake=True)
        return {"status": "ok", "action": "bake_all"}
    except Exception as e:
        return {"error": str(e)}


def add_force_field(type="FORCE", name=None, location=(0, 0, 0), strength=1.0):
    """Create a force field empty. type: FORCE, WIND, VORTEX, MAGNET, ..."""
    bpy.ops.object.effector_add(type=type, location=location)
    obj = bpy.context.active_object
    if name:
        obj.name = name
    if hasattr(obj, "field") and obj.field:
        obj.field.strength = strength
    return {"name": obj.name, "type": type, "strength": strength}


HANDLERS = {
    "add_rigid_body": add_rigid_body,
    "remove_rigid_body": remove_rigid_body,
    "add_cloth": add_cloth,
    "add_soft_body": add_soft_body,
    "add_collision": add_collision,
    "add_fluid_domain": add_fluid_domain,
    "add_fluid_flow": add_fluid_flow,
    "bake_physics": bake_physics,
    "add_force_field": add_force_field,
}
