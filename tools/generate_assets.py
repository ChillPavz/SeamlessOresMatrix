#!/usr/bin/env python3
"""
Generates Seamless Ores: Matrix's assets and data from the host table in HostStone.java:
blockstates, two-layer block models, item model definitions, the lang file, the overlay textures,
loot tables, tags, the config switches in both loaders' MatrixConfigData, and the README lists.

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
Transformed from the ore's own tables, never written by hand: the silk-touch branch drops our block,
everything else is the ore's. One set per era, because the format changed at 26.3:
  src/era263  from the 26.3 client jar; silk touch is "condition": "minecraft:tool/can_silk_touch".
  src/era261  from the 26.1.2 client jar (it spells out defaults 26.2 leaves implicit, and loads on
              both); silk touch is a minecraft:match_tool condition.
Zinc's tables come from Create's own jar and exist in era261 only: Create has no 26.3 release.
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
CONFIG_DATA = [os.path.join(ROOT, loader, "src", "main", "java", "com", "chillpavz", MOD_ID, "config",
                            "MatrixConfigData.java") for loader in ("fabric", "neoforge")]
ARTIFACTS = os.path.expanduser("~/.gradle/caches/neoformruntime/artifacts")
JARS = os.path.join(os.path.dirname(ROOT), "references", "jars")
# era -> the client jar its loot is read from
ERAS = {"263": os.path.join(ARTIFACTS, "minecraft_26.3_client.jar"),
        "261": os.path.join(ARTIFACTS, "minecraft_26.1.2_client.jar")}
CREATE_JAR = os.path.join(JARS, "26.1.2-create-fly-26.1.2-6.0.9-4.jar")
OVERLAYS = os.environ.get("OVERLAYS", os.path.join(
    os.path.dirname(ROOT), "seamless-glowing-ores", "assets", "overlays"))

# Every ore kind, in OreKind order. mod: the ore's own mod (None for vanilla); forms: the ore blocks,
# stone form first; loot: where its tables come from; overlay: the art, relative to OVERLAYS; tag: the
# c:ores/<tag> it belongs in; name: how it reads in a block name.
ORES = {
    "coal": {}, "iron": {}, "copper": {}, "gold": {}, "redstone": {}, "emerald": {},
    "lapis": {"name": "Lapis Lazuli"}, "diamond": {},
    "zinc": {"mod": "create", "forms": ["create:zinc_ore", "create:deepslate_zinc_ore"], "loot": "create",
             "overlay": "create/zinc_overlay.png"},
    "nether_gold": {"forms": ["minecraft:nether_gold_ore"], "tag": "gold"},
    "quartz": {"forms": ["minecraft:nether_quartz_ore"], "name": "Nether Quartz"},
}
for _ore, _info in ORES.items():
    _info.setdefault("mod", None)
    _info.setdefault("forms", [f"minecraft:{_ore}_ore", f"minecraft:deepslate_{_ore}_ore"])
    _info.setdefault("loot", "minecraft")
    _info.setdefault("overlay", f"vanilla/{_ore}_overlay.png")
    _info.setdefault("tag", _ore)
    _info.setdefault("name", " ".join(w.capitalize() for w in _ore.split("_")))

TOOL_TAGS = ["needs_stone_tool", "needs_iron_tool", "needs_diamond_tool"]
FACES = ["down", "up", "north", "south", "west", "east"]

# Display names of the mods that place the hosts, for the config screen and the README.
MOD_NAMES = {"blockus": "Blockus", "create": "Create", "forbidden_arcanus": "Forbidden and Arcanus",
             "mythicupgrades": "Mythic Upgrades", "promenade": "Promenade", "wilderwild": "Wilder Wild"}
# Where each of those mods exists at 26.x, measured with references/tools/som-grid/availability.py.
MOD_BANDS = {"blockus": "Fabric, 26.1.x to 26.3", "create": "Create Fly, Fabric, 26.1.2 and 26.2",
             "forbidden_arcanus": "NeoForge, 26.1.2", "mythicupgrades": "Fabric and NeoForge, 26.2",
             "promenade": "Fabric, 26.1.x and 26.2",
             "wilderwild": "Fabric 26.1.x to 26.3, NeoForge 26.2 and 26.3"}

# How each host is drawn, read from the stone mod's own blockstate. A host with several looks must be
# mirrored exactly, or its ore is the one tile that never varies.
#   single:          one texture.
#   mirrored_turned: Wilder Wild gabbro, four random models: plain, mirrored, and each turned 180.
#   textures4:       Create's natural stones, four random models, each its own texture (<prefix>0 to 3).
HOST_LOOK = {
    "blockus:limestone": ("blockus:block/limestone", "single"),
    "blockus:marble": ("blockus:block/marble", "single"),
    "blockus:bluestone": ("blockus:block/bluestone", "single"),
    "blockus:viridite": ("blockus:block/viridite", "single"),
    "create:asurine": ("create:block/palettes/stone_types/natural/asurine_", "textures4"),
    "create:crimsite": ("create:block/palettes/stone_types/natural/crimsite_", "textures4"),
    "create:limestone": ("create:block/palettes/stone_types/limestone", "single"),
    "create:ochrum": ("create:block/palettes/stone_types/natural/ochrum_", "textures4"),
    "create:scorchia": ("create:block/palettes/stone_types/scorchia", "single"),
    "create:scoria": ("create:block/palettes/stone_types/scoria", "single"),
    "create:veridium": ("create:block/palettes/stone_types/natural/veridium_", "textures4"),
    "minecraft:calcite": ("minecraft:block/calcite", "single"),
    "minecraft:dripstone_block": ("minecraft:block/dripstone_block", "single"),
    "minecraft:smooth_basalt": ("minecraft:block/smooth_basalt", "single"),
    "forbidden_arcanus:darkstone": ("forbidden_arcanus:block/darkstone", "single"),
    "mythicupgrades:aquamarine_schist": ("mythicupgrades:block/aquamarine_schist", "single"),
    "mythicupgrades:citrine_schist": ("mythicupgrades:block/citrine_schist", "single"),
    "mythicupgrades:peridot_schist": ("mythicupgrades:block/peridot_schist", "single"),
    "mythicupgrades:topaz_schist": ("mythicupgrades:block/topaz_schist", "single"),
    "promenade:asphalt": ("promenade:block/asphalt", "single"),
    "promenade:blunite": ("promenade:block/blunite", "single"),
    "wilderwild:gabbro": ("wilderwild:block/gabbro", "mirrored_turned"),
}

# A stone whose display name is not its id, title-cased.
STONE_NAMES = {"dripstone_block": "Dripstone"}


def read_hosts():
    """(namespace, path, placing mod, strength, [ores]) per host, parsed from HostStone.java."""
    text = open(HOST_TABLE, encoding="utf-8").read()
    pattern = re.compile(r'new HostStone\("(\w+)",\s*"(\w+)",\s*Strength\.(\w+),\s*MapColor\.\w+,\s*'
                         r'EnumSet\.of\(([^)]*)\)\)(\s*\.placedBy\("(\w+)"\))?\s*;', re.S)
    hosts = []
    for ns, path, strength, ores, _p, placed in pattern.findall(text):
        listed = [o.strip().lower() for o in ores.split(",")]
        unknown = [o for o in listed if o not in ORES]
        if unknown:
            sys.exit(f"{ns}:{path} lists unknown ores {unknown}")
        hosts.append((ns, path, placed or ns, strength.lower(), [o for o in ORES if o in listed]))
    declared = len(re.findall(r"new HostStone\(\"", text))
    if len(hosts) != declared:
        sys.exit(f"parsed {len(hosts)} of {declared} hosts in {HOST_TABLE}: keep each one the shape"
                 f' new HostStone("ns", "path", Strength.X, MapColor.Y, EnumSet.of(...))[.placedBy("mod")];')
    return hosts


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def faces(texture, mirrored=False):
    uv = [16, 0, 0, 16] if mirrored else [0, 0, 16, 16]
    return {side: {"uv": uv, "texture": texture, "cullface": side} for side in FACES}


def model(stone, ore, mirrored=False):
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


def stone_name(path):
    return STONE_NAMES.get(path) or " ".join(w.capitalize() for w in path.split("_"))


def camel(*parts):
    words = "_".join(parts).split("_")
    return words[0] + "".join(w[:1].upper() + w[1:] for w in words[1:])


def ore_source(ore, strength):
    """The ore block whose loot and tool tier a variant takes: the deepslate form for a deepslate host."""
    forms = ORES[ore]["forms"]
    return forms[1] if strength == "deepslate" and len(forms) > 1 else forms[0]


def loot_table(jars, era, ore, strength):
    """The ore's own table for this era, or None if the ore has none in that era."""
    ns, name = ore_source(ore, strength).split(":")
    if ORES[ore]["loot"] == "create":
        if era != "261":
            return None
        jar = jars["create"]
    else:
        jar = jars[era]
    return json.load(jar.open(f"data/{ns}/loot_table/blocks/{name}.json"))


def main():
    hosts = read_hosts()
    for ns, path, *_rest in hosts:
        if f"{ns}:{path}" not in HOST_LOOK:
            sys.exit(f"{ns}:{path} has no HOST_LOOK entry")
    for jar in list(ERAS.values()) + [CREATE_JAR]:
        if not os.path.exists(jar):
            sys.exit(f"jar not found: {jar}")
    paths = [path for _ns, path, *_r in hosts]
    clashes = {p for p in paths if paths.count(p) > 1}

    assets = os.path.join(COMMON, "assets", MOD_ID)
    data = os.path.join(COMMON, "data")
    era_data = {era: os.path.join(ROOT, "common", "src", f"era{era}", "resources", "data") for era in ERAS}
    # Generated folders are rebuilt from scratch, so a host or ore taken out of the table leaves no file.
    for sub in ("blockstates", "models", "items", "textures"):
        shutil.rmtree(os.path.join(assets, sub), ignore_errors=True)
    for sub in ("c", "minecraft"):
        shutil.rmtree(os.path.join(data, sub), ignore_errors=True)
    for root in era_data.values():
        shutil.rmtree(os.path.join(root, MOD_ID, "loot_table"), ignore_errors=True)

    lang = {f"itemGroup.{MOD_ID}.ores": "Seamless Ores: Matrix"}
    mineable, tool_tags, conv = [], {}, {}
    used_overlays = set()
    count = 0

    jars = {era: zipfile.ZipFile(path) for era, path in ERAS.items()}
    jars["create"] = zipfile.ZipFile(CREATE_JAR)
    # Tool tiers from the ore's own mod: vanilla's tags, and Create's for zinc.
    tool_members = {}
    for tag in TOOL_TAGS:
        members = set()
        for jar in (jars["263"], jars["create"]):
            name = f"data/minecraft/tags/block/{tag}.json"
            if name in jar.namelist():
                members |= set(json.load(jar.open(name))["values"])
        tool_members[tag] = members

    for ns, path, placer, strength, kinds in hosts:
        stone, look = HOST_LOOK[f"{ns}:{path}"]
        for ore in kinds:
            info = ORES[ore]
            name = f"{ns}_{path}_{ore}_ore"
            our_id = f"{MOD_ID}:{name}"
            base = f"{MOD_ID}:block/{name}"
            used_overlays.add(ore)

            models = os.path.join(assets, "models", "block")
            if look == "single":
                state = {"variants": {"": {"model": base}}}
                write_json(os.path.join(models, f"{name}.json"), model(stone, ore))
            elif look == "mirrored_turned":
                state = {"variants": {"": [{"model": base}, {"model": base + "_mirrored"},
                                           {"model": base, "y": 180}, {"model": base + "_mirrored", "y": 180}]}}
                write_json(os.path.join(models, f"{name}.json"), model(stone, ore))
                write_json(os.path.join(models, f"{name}_mirrored.json"), model(stone, ore, True))
            elif look == "textures4":
                # Create picks one of four natural textures per block; ours picks the same way, so a
                # vein does not show as the one repeated tile in a varied wall.
                state = {"variants": {"": [{"model": f"{base}_{i}"} for i in range(4)]}}
                for i in range(4):
                    write_json(os.path.join(models, f"{name}_{i}.json"), model(f"{stone}{i}", ore))
                # The item needs one model to point at.
                write_json(os.path.join(models, f"{name}.json"), model(f"{stone}0", ore))
            else:
                sys.exit(f"unknown look {look}")
            write_json(os.path.join(assets, "blockstates", f"{name}.json"), state)
            write_json(os.path.join(assets, "items", f"{name}.json"),
                       {"model": {"type": "minecraft:model", "model": base}})
            # Create and Blockus both have a limestone; a clashing stone name carries its mod.
            clash = f" ({MOD_NAMES[placer]})" if path in clashes else ""
            lang[f"block.{MOD_ID}.{name}"] = f"{stone_name(path)} {info['name']} Ore{clash}"

            # The strength source is also the loot source; the two tiers drop the same items.
            # From 26.3 loot tables are a datapack REGISTRY, and a table naming an item that is not
            # registered fails registry loading: the world does not open. A variant is only registered
            # when the mod that places its stone (and a modded ore's own mod) is installed, so every
            # table is gated on exactly that.
            gate = [placer] + ([info["mod"]] if info["mod"] and info["mod"] != placer else [])
            for era in ERAS:
                table = loot_table(jars, era, ore, strength)
                if table is None:
                    continue
                silk = 0
                for pool in table.get("pools", []):
                    for entry in pool.get("entries", []):
                        for child in entry.get("children", []):
                            if is_silk_touch_branch(child):
                                child["name"] = our_id
                                silk += 1
                if silk != 1:
                    sys.exit(f"{ore_source(ore, strength)} ({era}): expected one silk touch branch, found {silk}")
                table["random_sequence"] = f"{MOD_ID}:blocks/{name}"
                table = {
                    "fabric:load_conditions": [{"condition": "fabric:registry_contains",
                                                "registry": "minecraft:block", "values": [our_id]}],
                    "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": m} for m in gate],
                    **table,
                }
                write_json(os.path.join(era_data[era], MOD_ID, "loot_table", "blocks", f"{name}.json"), table)

            # Optional entries: a variant only exists when its mods are installed, and a required entry
            # naming an absent block fails the whole tag.
            entry = {"id": our_id, "required": False}
            mineable.append(entry)
            for tag, members in tool_members.items():
                if ore_source(ore, strength) in members:
                    tool_tags.setdefault(tag, []).append(entry)
            conv.setdefault(info["tag"], []).append(entry)
            count += 1

    # Config screen text. Field names follow MatrixConfigData: the host's name in camelCase, one per
    # host stone, in a category named after the mod that places it.
    cfg = f"text.autoconfig.{MOD_ID}"
    lang[f"{cfg}.title"] = "Seamless Ores: Matrix"
    for ns, path, placer, _strength, _kinds in hosts:
        lang[f"{cfg}.category.{placer}"] = MOD_NAMES[placer]
        field = camel(ns, path)
        lang[f"{cfg}.option.{field}"] = stone_name(path)
        where = MOD_NAMES[placer] if placer == ns else f"{MOD_NAMES[placer]}'s bands of"
        lang[f"{cfg}.option.{field}.@Tooltip"] = (
            f"Ore generated in {where} {stone_name(path).lower()} matches the stone. Off: it keeps"
            f" its vanilla look. Applies to newly generated chunks, from the next world load.")

    lang = dict(sorted(lang.items()))
    for key, value in lang.items():
        if any(ch in value for ch in (chr(0x2013), chr(0x2014))):
            sys.exit(f"dash in public text: {key}")
    write_json(os.path.join(assets, "lang", "en_us.json"), lang)

    textures = os.path.join(assets, "textures", "block")
    os.makedirs(textures, exist_ok=True)
    for ore in sorted(used_overlays):
        source = os.path.join(OVERLAYS, ORES[ore]["overlay"])
        if not os.path.exists(source):
            sys.exit(f"overlay missing: {source}")
        shutil.copyfile(source, os.path.join(textures, f"{ore}_overlay.png"))

    write_json(os.path.join(data, "minecraft", "tags", "block", "mineable", "pickaxe.json"), {"values": mineable})
    for tag, values in tool_tags.items():
        write_json(os.path.join(data, "minecraft", "tags", "block", f"{tag}.json"), {"values": values})
    everything = sorted(mineable, key=lambda e: e["id"])
    for kind in ("block", "item"):
        write_json(os.path.join(data, "c", "tags", kind, "ores.json"), {"values": everything})
        for tag, values in conv.items():
            write_json(os.path.join(data, "c", "tags", kind, "ores", f"{tag}.json"), {"values": values})

    write_config(hosts)
    write_readme(hosts, count, [o for o in ORES if o in used_overlays], clashes)

    per_mod = {}
    for _ns, _path, placer, _s, kinds in hosts:
        per_mod[placer] = per_mod.get(placer, 0) + len(kinds)
    print(f"{count} variants ({', '.join(f'{m} {n}' for m, n in per_mod.items())}); "
          f"{len(used_overlays)} overlays; loot eras {', '.join(ERAS)}")


def write_config(hosts):
    """Writes the switches and push() of both loaders' MatrixConfigData, which must stay identical.

    Category order is field order, so the hosts are written grouped by the mod that places them, in
    the host table's order (which is alphabetical by mod display name).
    """
    fields, push = [], []
    for placer in dict.fromkeys(h[2] for h in hosts):
        bar = f"    // --- {MOD_NAMES[placer]} "
        fields += [bar + "-" * (104 - len(bar)), ""]
        for ns, path, p, _s, _k in hosts:
            if p != placer:
                continue
            field = camel(ns, path)
            fields += [f'    @ConfigEntry.Category("{placer}")', "    @ConfigEntry.Gui.Tooltip",
                       f"    public boolean {field} = true;", ""]
            push.append(f'        values.put("{ns}_{path}", {field});')
    texts = []
    for path in CONFIG_DATA:
        text = open(path, encoding="utf-8").read()
        text = replace_block(text, "    // BEGIN GENERATED switches (tools/generate_assets.py, from the host table)\n",
                             "    // END GENERATED switches", "\n".join(fields), path)
        text = replace_block(text, "        // BEGIN GENERATED push\n", "        // END GENERATED push",
                             "\n".join(push) + "\n", path)
        texts.append(text)
    if texts[0] != texts[1]:
        sys.exit("the two MatrixConfigData copies differ outside the generated blocks; make them identical")
    for path, text in zip(CONFIG_DATA, texts):
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)


def replace_block(text, begin, end, body, where):
    if begin not in text or end not in text:
        sys.exit(f"{where} has no '{begin.strip()}' markers")
    head, rest = text.split(begin, 1)
    _old, tail = rest.split(end, 1)
    return f"{head}{begin}{body}{end}{tail}"


def write_readme(hosts, count, overlays, clashes):
    """Rewrites the generated sections of README.md in place, leaving the prose alone.

    The block list and the overlay list come from the same host table the blocks register from, so
    the README cannot claim a block the jar does not have. A missing marker is an error, not a skip.
    """
    path = os.path.join(ROOT, "README.md")
    text = open(path, encoding="utf-8").read()

    lines = [f"**{count} blocks** in the `{MOD_ID}` namespace. Each exists only when the mod that places "
             f"its stone is installed, and a zinc one only with Create as well.", ""]
    for placer in dict.fromkeys(h[2] for h in hosts):
        stones = [(ns, p, k) for ns, p, pl, _s, k in hosts if pl == placer]
        lines.append(f"**{MOD_NAMES[placer]}, requires `{placer}`** ({MOD_BANDS[placer]})")
        lines.append("")
        lines.append("| | " + " | ".join(stone_name(p) for _ns, p, _k in stones) + " |")
        lines.append("|---" * (len(stones) + 1) + "|")
        for ore in ORES:
            if not any(ore in k for _ns, _p, k in stones):
                continue
            cells = [f"`{ns}_{p}_{ore}_ore`" if ore in k else "" for ns, p, k in stones]
            lines.append(f"| {ORES[ore]['name']} | " + " | ".join(cells) + " |")
        lines.append("")
    text = replace_section(text, "block-list", "\n".join(lines).rstrip())

    listed = " ".join(f"`{o}`" for o in overlays)
    fence = "```"
    text = replace_section(text, "overlay-list", (
        f"Every variant of one ore shares a single overlay texture, so covering all {count} blocks "
        f"takes **{len(overlays)} PNG files**:\n\n{fence}\nassets/{MOD_ID}/textures/block/<ore>_overlay.png\n"
        f"{fence}\n\nwhere `<ore>` is one of: {listed}"))

    if any(ch in text for ch in (chr(0x2013), chr(0x2014))):
        sys.exit("dash in README.md")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def replace_section(text, name, body):
    begin, end = f"<!-- BEGIN GENERATED {name} -->", f"<!-- END GENERATED {name} -->"
    if begin not in text or end not in text:
        sys.exit(f"README.md has no {name} markers")
    head, rest = text.split(begin, 1)
    _old, tail = rest.split(end, 1)
    return f"{head}{begin}\n{body}\n{end}{tail}"


if __name__ == "__main__":
    main()
