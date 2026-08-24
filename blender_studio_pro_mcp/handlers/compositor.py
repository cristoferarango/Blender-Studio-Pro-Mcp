"""Compositor node tree helpers."""

from __future__ import annotations

import bpy


def ensure_compositor():
    scene = bpy.context.scene
    scene.use_nodes = True
    tree = scene.node_tree
    return {"enabled": True, "tree": tree.name if tree else None}


def get_compositor_tree():
    scene = bpy.context.scene
    if not scene.use_nodes or not scene.node_tree:
        return {"error": "Compositor nodes not enabled. Call ensure_compositor()."}
    tree = scene.node_tree
    nodes = []
    for n in tree.nodes:
        nodes.append({
            "name": n.name,
            "type": n.bl_idname,
            "location": list(n.location),
        })
    links = []
    for l in tree.links:
        links.append({
            "from": f"{l.from_node.name}.{l.from_socket.name}",
            "to": f"{l.to_node.name}.{l.to_socket.name}",
        })
    return {"nodes": nodes, "links": links}


def add_compositor_node(node_type, location=(0, 0), name=None):
    """node_type e.g. CompositorNodeRLayers, CompositorNodeBlur, CompositorNodeComposite."""
    scene = bpy.context.scene
    scene.use_nodes = True
    tree = scene.node_tree
    node = tree.nodes.new(type=node_type)
    node.location = location
    if name:
        node.name = name
    return {"name": node.name, "type": node.bl_idname}


def connect_compositor_nodes(from_node, from_socket, to_node, to_socket):
    tree = bpy.context.scene.node_tree
    if not tree:
        return {"error": "No compositor tree"}
    a = tree.nodes.get(from_node)
    b = tree.nodes.get(to_node)
    if not a or not b:
        return {"error": "Node not found"}
    fs = a.outputs.get(from_socket) if hasattr(a.outputs, "get") else None
    ts = b.inputs.get(to_socket) if hasattr(b.inputs, "get") else None
    if fs is None:
        fs = next((s for s in a.outputs if s.name == from_socket), None)
    if ts is None:
        ts = next((s for s in b.inputs if s.name == to_socket), None)
    if fs is None or ts is None:
        return {"error": "Socket not found"}
    tree.links.new(fs, ts)
    return {"linked": f"{from_node}.{from_socket} -> {to_node}.{to_socket}"}


def set_compositor_node_input(node_name, input_name, value):
    tree = bpy.context.scene.node_tree
    if not tree:
        return {"error": "No compositor tree"}
    node = tree.nodes.get(node_name)
    if not node:
        return {"error": f"Node '{node_name}' not found"}
    sock = node.inputs.get(input_name) if hasattr(node.inputs, "get") else None
    if sock is None:
        sock = next((s for s in node.inputs if s.name == input_name), None)
    if sock is None:
        return {"error": f"Input '{input_name}' not found"}
    sock.default_value = value
    return {"node": node_name, "input": input_name, "value": value}


HANDLERS = {
    "ensure_compositor": ensure_compositor,
    "get_compositor_tree": get_compositor_tree,
    "add_compositor_node": add_compositor_node,
    "connect_compositor_nodes": connect_compositor_nodes,
    "set_compositor_node_input": set_compositor_node_input,
}
