"""Particle systems and hair."""

from __future__ import annotations

import bpy


def add_particle_system(object_name, name="ParticleSystem", type="EMITTER", count=1000):
    """type: EMITTER or HAIR."""
    obj = bpy.data.objects.get(object_name)
    if not obj or obj.type != "MESH":
        return {"error": "Mesh object required"}
    mod = obj.modifiers.new(name=name, type="PARTICLE_SYSTEM")
    psys = obj.particle_systems[-1]
    settings = psys.settings
    settings.type = type
    settings.count = count
    return {
        "object": object_name,
        "system": psys.name,
        "settings": settings.name,
        "type": type,
        "count": count,
    }


def set_particle_settings(object_name, system_name=None, **params):
    """Set particle settings attributes (count, lifetime, frame_start, ...)."""
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    if not obj.particle_systems:
        return {"error": "No particle systems on object"}
    psys = obj.particle_systems.get(system_name) if system_name else obj.particle_systems[0]
    if not psys:
        return {"error": f"Particle system '{system_name}' not found"}
    settings = psys.settings
    applied = {}
    for k, v in params.items():
        if hasattr(settings, k):
            setattr(settings, k, v)
            applied[k] = v
    return {"object": object_name, "system": psys.name, "applied": applied}


def list_particle_systems(object_name):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    return {
        "object": object_name,
        "systems": [
            {"name": p.name, "settings": p.settings.name, "type": p.settings.type}
            for p in obj.particle_systems
        ],
    }


def remove_particle_system(object_name, system_name=None):
    obj = bpy.data.objects.get(object_name)
    if not obj:
        return {"error": f"Object '{object_name}' not found"}
    if not obj.particle_systems:
        return {"error": "No particle systems"}
    psys = obj.particle_systems.get(system_name) if system_name else obj.particle_systems[0]
    if not psys:
        return {"error": "System not found"}
    name = psys.name
    obj.modifiers.remove(obj.modifiers.get(name) or obj.modifiers[-1])
    return {"removed": name}


HANDLERS = {
    "add_particle_system": add_particle_system,
    "set_particle_settings": set_particle_settings,
    "list_particle_systems": list_particle_systems,
    "remove_particle_system": remove_particle_system,
}
