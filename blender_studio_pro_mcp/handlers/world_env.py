"""World / environment / color management."""

from __future__ import annotations

import bpy


def get_world_info():
    world = bpy.context.scene.world
    if not world:
        return {"error": "No world in scene"}
    info = {"name": world.name, "use_nodes": world.use_nodes}
    if world.use_nodes and world.node_tree:
        info["nodes"] = [n.name for n in world.node_tree.nodes]
    return info


def ensure_world(name="World"):
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new(name)
        bpy.context.scene.world = world
    world.use_nodes = True
    return {"name": world.name}


def set_world_background(color=(0.05, 0.05, 0.05, 1.0), strength=1.0):
    """Set Background shader color/strength on the world."""
    ensure_world()
    world = bpy.context.scene.world
    tree = world.node_tree
    bg = None
    for n in tree.nodes:
        if n.type == "BACKGROUND":
            bg = n
            break
    if bg is None:
        bg = tree.nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = color
    bg.inputs["Strength"].default_value = strength
    return {"color": list(color), "strength": strength}


def set_hdri(filepath, strength=1.0):
    """Load an HDRI/environment texture into the world."""
    ensure_world()
    world = bpy.context.scene.world
    tree = world.node_tree
    tree.nodes.clear()
    output = tree.nodes.new("ShaderNodeOutputWorld")
    bg = tree.nodes.new("ShaderNodeBackground")
    env = tree.nodes.new("ShaderNodeTexEnvironment")
    mapping = tree.nodes.new("ShaderNodeMapping")
    texcoord = tree.nodes.new("ShaderNodeTexCoord")
    try:
        img = bpy.data.images.load(filepath)
        env.image = img
    except Exception as e:
        return {"error": f"Failed to load image: {e}"}
    tree.links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
    tree.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    tree.links.new(env.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    tree.links.new(bg.outputs["Background"], output.inputs["Surface"])
    return {"filepath": filepath, "strength": strength, "image": img.name}


def set_color_management(display_device=None, view_transform=None, look=None, exposure=None, gamma=None):
    vs = bpy.context.scene.view_settings
    applied = {}
    if display_device is not None:
        bpy.context.scene.display_settings.display_device = display_device
        applied["display_device"] = display_device
    if view_transform is not None:
        vs.view_transform = view_transform
        applied["view_transform"] = view_transform
    if look is not None:
        vs.look = look
        applied["look"] = look
    if exposure is not None:
        vs.exposure = exposure
        applied["exposure"] = exposure
    if gamma is not None:
        vs.gamma = gamma
        applied["gamma"] = gamma
    return applied


HANDLERS = {
    "get_world_info": get_world_info,
    "ensure_world": ensure_world,
    "set_world_background": set_world_background,
    "set_hdri": set_hdri,
    "set_color_management": set_color_management,
}
