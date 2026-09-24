#!/usr/bin/env python3
"""
Generates Seamless Ores: Matrix's assets and data from the host table in HostStone.java:
blockstates, two-layer block models, item model definitions, the lang file, the overlay textures,
loot tables and tags.

    python tools/generate_assets.py

The host table is READ from common/.../content/HostStone.java, so the blocks that register and the
files generated here cannot drift apart.

Textures
--------
Only the overlays ship. They are the owner's own art, shared with Seamless Ores and Seamless
Glowing Ores, and copied from the pack's overlay folder. Every host stone is referenced by its id
(blockus:block/limestone) and none of its pixels ship: the stone's mod draws it.

Loot
----
Transformed from vanilla's own tables in the 26.3 client jar, never written by hand: the silk-touch
branch drops our block, everything else is the vanilla ore's. 26.3 writes silk touch as a single
"condition": "minecraft:tool/can_silk_touch".
"""

import json
import os
import re
import shutil
import sys
import zipfile

MOD_ID = "seamlessoresmatrix"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMON = os.path.join(ROOT, "common", "src", "main", "resources")
HOST_TABLE = os.path.join(ROOT, "common", "src", "main", "java", "com", "chillpavz", MOD_ID,
                          "content", "HostStone.java")
CLIENT_JAR = os.path.expanduser("~/.gradle/caches/neoformruntime/artifacts/minecraft_26.3_client.jar")
OVERLAYS = os.environ.get("OVERLAYS", os.path.join(
    ROOT, "..", "seamless-glowing-ores", "assets", "overlays", "vanilla"))

ORES = ["coal", "iron", "copper", "gold", "redstone", "emerald", "lapis", "diamond"]
TOOL_TAGS = ["needs_stone_tool", "needs_iron_tool", "needs_diamond_tool"]
FACES = ["down", "up", "north", "south", "west", "east"]

# How each host is drawn, read from the stone mod's own blockstate. A host with several looks must be
# mirrored exactly, or its ore is the one tile that never varies.
#   single:          {"": model}
#   mirrored_turned: Wilder Wild gabbro, four random models: plain, mirrored, and each turned 180.
# Display names of the stone mods, for the config screen.
MOD_NAMES = {"blockus": "Blockus", "wilderwild": "Wilder Wild"}

HOST_LOOK = {
    "blockus:limestone": ("blockus:block/limestone", "single"),
    "blockus:marble": ("blockus:block/marble", "single"),
    "blockus:bluestone": ("blockus:block/bluestone", "single"),
    "blockus:viridite": ("blockus:block/viridite", "single"),
    "wilderwild:gabbro": ("wilderwild:block/gabbro", "mirrored_turned"),
}

DISPLAY = {"lapis": "Lapis Lazuli"}


def read_hosts():
    """(mod, path, strength, [ores]) per host, parsed from HostStone.java."""
    text = open(HOST_TABLE, encoding="utf-8").read()
    hosts = []
    pattern = re.compile(r'new HostStone\("(\w+)", "(\w+)",\s*Strength\.(\w+), MapColor\.\w+,\s*(.*?)\);', re.S)
    for mod, path, strength, ores in pattern.findall(text):
        ores = " ".join(ores.split())
        listed = [o.lower() for o in re.findall(r"OreKind\.(\w+)", ores)]
        if ores == "EnumSet.allOf(OreKind.class)":
            kinds = list(ORES)
        elif ores.startswith("EnumSet.complementOf"):
            kinds = [o for o in ORES if o not in listed]
        elif ores.startswith("EnumSet.of"):
            kinds = [o for o in ORES if o in listed]
        else:
            sys.exit(f"cannot read the ore list of {mod}:{path}: {ores}")
        hosts.append((mod, path, strength.lower(), kinds))
    if not hosts:
        sys.exit(f"no hosts found in {HOST_TABLE}")
    return hosts


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def faces(texture, mirrored=False):
    uv = [16, 0, 0, 16] if mirrored else [0, 0, 16, 16]
    return {side: {"uv": uv, "texture": texture, "cullface": side} for side in FACES}


def model(stone, ore, mirrored):
    """Two coincident cubes, like vanilla's grass block: the stone, then the ore overlay.

    No render_type: from 26.1 the chunk layer is derived from each texture's own alpha, so the
    overlay lands on cutout by itself. Only the stone layer is mirrored in the mirrored model: it has
    to match the host tile beside it exactly, while the ore art reads the same either way.
    """
    return {
        "parent": "minecraft:block/block",
        "textures": {"particle": stone, "stone": stone, "overlay": f"{MOD_ID}:block/{ore}_overlay"},
        "elements": [
            {"from": [0, 0, 0], "to": [16, 16, 16], "faces": faces("#stone", mirrored)},
            {"from": [0, 0, 0], "to": [16, 16, 16], "faces": faces("#overlay")},
        ],
    }


def is_silk_touch_branch(child):
    condition = child.get("condition")
    if isinstance(condition, str):
        return condition.endswith("can_silk_touch")
    if isinstance(condition, dict):
        return condition.get("type") == "minecraft:match_tool"
    return any(c.get("condition") == "minecraft:match_tool" for c in child.get("conditions", []))


def title(name):
    return " ".join(DISPLAY.get(part, part.capitalize()) for part in name.split("_"))


def main():
    hosts = read_hosts()
    for mod, path, _s, _o in hosts:
        if f"{mod}:{path}" not in HOST_LOOK:
            sys.exit(f"{mod}:{path} has no HOST_LOOK entry")
    if not os.path.exists(CLIENT_JAR):
        sys.exit(f"client jar not found at {CLIENT_JAR}")

    assets = os.path.join(COMMON, "assets", MOD_ID)
    data = os.path.join(COMMON, "data")
    # Generated folders are rebuilt from scratch, so a host or ore taken out of the table leaves no file.
    for sub in ("blockstates", "models", "items", "textures"):
        shutil.rmtree(os.path.join(assets, sub), ignore_errors=True)
    for sub in (os.path.join(MOD_ID, "loot_table"), "c", "minecraft"):
        shutil.rmtree(os.path.join(data, sub), ignore_errors=True)

    lang = {f"itemGroup.{MOD_ID}.ores": "Seamless Ores: Matrix"}
    mineable, tool_tags, conv = [], {}, {}
    used_overlays = set()
    count = 0

    with zipfile.ZipFile(CLIENT_JAR) as jar:
        vanilla_tools = {tag: set(json.load(jar.open(f"data/minecraft/tags/block/{tag}.json"))["values"])
                         for tag in TOOL_TAGS}
        for mod, path, strength, kinds in hosts:
            stone, look = HOST_LOOK[f"{mod}:{path}"]
            for ore in kinds:
                name = f"{mod}_{path}_{ore}_ore"
                our_id = f"{MOD_ID}:{name}"
                base = f"{MOD_ID}:block/{name}"
                used_overlays.add(ore)

                if look == "single":
                    state = {"variants": {"": {"model": base}}}
                else:
                    state = {"variants": {"": [{"model": base}, {"model": base + "_mirrored"},
                                               {"model": base, "y": 180}, {"model": base + "_mirrored", "y": 180}]}}
                    write_json(os.path.join(assets, "models", "block", f"{name}_mirrored.json"),
                               model(stone, ore, True))
                write_json(os.path.join(assets, "blockstates", f"{name}.json"), state)
                write_json(os.path.join(assets, "models", "block", f"{name}.json"), model(stone, ore, False))
                write_json(os.path.join(assets, "items", f"{name}.json"),
                           {"model": {"type": "minecraft:model", "model": base}})
                lang[f"block.{MOD_ID}.{name}"] = title(f"{path}_{ore}_ore")

                # The strength source is also the loot source; the two tiers drop the same items.
                vanilla = f"{ore}_ore" if strength == "stone" else f"deepslate_{ore}_ore"
                table = json.load(jar.open(f"data/minecraft/loot_table/blocks/{vanilla}.json"))
                silk = 0
                for pool in table.get("pools", []):
                    for entry in pool.get("entries", []):
                        for child in entry.get("children", []):
                            if is_silk_touch_branch(child):
                                child["name"] = our_id
                                silk += 1
                if silk != 1:
                    sys.exit(f"{vanilla}: expected one silk touch branch, found {silk}")
                table["random_sequence"] = f"{MOD_ID}:blocks/{name}"
                # From 26.3 loot tables are a datapack REGISTRY, and a table naming an item that is
                # not registered fails registry loading: the world does not open. A variant is only
                # registered when its stone's mod is installed, so every table is gated on that.
                table = {
                    "fabric:load_conditions": [{"condition": "fabric:registry_contains",
                                                "registry": "minecraft:block", "values": [our_id]}],
                    "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": mod}],
                    **table,
                }
                write_json(os.path.join(data, MOD_ID, "loot_table", "blocks", f"{name}.json"), table)

                # Optional entries: a variant only exists when its stone's mod is installed, and a
                # required entry naming an absent block fails the whole tag.
                entry = {"id": our_id, "required": False}
                mineable.append(entry)
                for tag, members in vanilla_tools.items():
                    if f"minecraft:{vanilla}" in members:
                        tool_tags.setdefault(tag, []).append(entry)
                conv.setdefault(ore, []).append(entry)
                count += 1

    # Config screen text. Field names follow MatrixConfigData: <mod><Path>, one per host stone, in a
    # category named after the stone's mod id.
    cfg = f"text.autoconfig.{MOD_ID}"
    lang[f"{cfg}.title"] = "Seamless Ores: Matrix"
    for mod, path, _strength, _kinds in hosts:
        lang[f"{cfg}.category.{mod}"] = MOD_NAMES[mod]
        field = mod + path[:1].upper() + path[1:]
        lang[f"{cfg}.option.{field}"] = title(path)
        lang[f"{cfg}.option.{field}.@Tooltip"] = (
            f"Ore generated in {MOD_NAMES[mod]} {title(path).lower()} matches the stone. Off: it keeps"
            f" its vanilla look. Applies to newly generated chunks, from the next world load.")

    lang = dict(sorted(lang.items()))
    for key, value in lang.items():
        if any(ch in value for ch in (chr(0x2013), chr(0x2014))):
            sys.exit(f"dash in public text: {key}")
    write_json(os.path.join(assets, "lang", "en_us.json"), lang)

    textures = os.path.join(assets, "textures", "block")
    os.makedirs(textures, exist_ok=True)
    for ore in sorted(used_overlays):
        source = os.path.join(OVERLAYS, f"{ore}_overlay.png")
        if not os.path.exists(source):
            sys.exit(f"overlay missing: {source}")
        shutil.copyfile(source, os.path.join(textures, f"{ore}_overlay.png"))

    write_json(os.path.join(data, "minecraft", "tags", "block", "mineable", "pickaxe.json"), {"values": mineable})
    for tag, values in tool_tags.items():
        write_json(os.path.join(data, "minecraft", "tags", "block", f"{tag}.json"), {"values": values})
    everything = sorted(mineable, key=lambda e: e["id"])
    for kind in ("block", "item"):
        write_json(os.path.join(data, "c", "tags", kind, "ores.json"), {"values": everything})
        for ore, values in conv.items():
            write_json(os.path.join(data, "c", "tags", kind, "ores", f"{ore}.json"), {"values": values})

    per_host = ", ".join(f"{mod}:{path} {len(kinds)}" for mod, path, _s, kinds in hosts)
    print(f"{count} variants ({per_host}); {len(used_overlays)} overlays")


if __name__ == "__main__":
    main()
