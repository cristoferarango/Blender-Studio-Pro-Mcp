from . import (
    bridge,
    scene,
    objects,
    materials,
    shader_nodes,
    lights,
    modifiers,
    animation,
    geometry_nodes,
    camera,
    render,
    io_handlers,
    code_exec,
    uv_texture,
    batch,
    assets,
    rigging,
    physics,
    particles,
    grease_pencil,
    sculpt_paint,
    compositor,
    sequencer,
    constraints,
    shapekeys,
    world_env,
    mesh_edit,
    curves_text,
    viewport,
    files_blend,
    timeline,
    collections_adv,
    drivers_props,
)

_MODULES = [
    bridge,
    scene,
    objects,
    materials,
    shader_nodes,
    lights,
    modifiers,
    animation,
    geometry_nodes,
    camera,
    render,
    io_handlers,
    code_exec,
    uv_texture,
    batch,
    assets,
    rigging,
    physics,
    particles,
    grease_pencil,
    sculpt_paint,
    compositor,
    sequencer,
    constraints,
    shapekeys,
    world_env,
    mesh_edit,
    curves_text,
    viewport,
    files_blend,
    timeline,
    collections_adv,
    drivers_props,
]

_REGISTRY = {}

for mod in _MODULES:
    if hasattr(mod, "HANDLERS"):
        _REGISTRY.update(mod.HANDLERS)


def dispatch_command(cmd):
    command_name = cmd.get("command")
    params = cmd.get("params", {})

    if not command_name:
        raise ValueError("No 'command' field in request")

    handler = _REGISTRY.get(command_name)
    if not handler:
        available = sorted(_REGISTRY.keys())
        raise ValueError(
            f"Unknown command: '{command_name}'. "
            f"Available commands ({len(available)}): {', '.join(available)}"
        )

    return handler(**params)


def list_registered_commands():
    """Return all dedicated MCP handler command names grouped by module."""
    grouped = {}
    for mod in _MODULES:
        if hasattr(mod, "HANDLERS"):
            grouped[mod.__name__.split(".")[-1]] = sorted(mod.HANDLERS.keys())
    return {
        "total": len(_REGISTRY),
        "modules": len(grouped),
        "by_module": grouped,
        "commands": sorted(_REGISTRY.keys()),
    }
