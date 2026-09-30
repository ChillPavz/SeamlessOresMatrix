#!/usr/bin/env python3
"""
Generates Seamless Ores: Matrix's assets and data from the host table in HostStone.java and the
modded pairs in tools/modded_pairs.json: blockstates, two-layer block models, item model
definitions, the lang file, the overlay textures, loot tables, tags, the generated Java (the modded
OreKind constants, ModdedPairs, the config switches in both loaders' MatrixConfigData), and the
README lists.

    python tools/generate_assets.py

The host table is READ from common/.../content/HostStone.java, so the blocks that register and the
files generated here cannot drift apart. The vanilla ores and zinc are written in that table by
hand; every other ore mod's pairs come from tools/modded_pairs.json, which the pair model writes
from the real jars (placement, biomes, feature order) and which carries each ore's forms, XP and
strength as Seamless Ores has them. Nothing in that file is edited by hand.

Textures
--------
Only the overlays ship. They are the owner's own art, shared with Seamless Ores and Seamless
Glowing Ores: the vanilla ores' and zinc's copied from the pack's overlay folder, every other mod's
from Seamless Ores' own 26.x textures, where each already carries its unique key. Translucent opal
takes a precomposited overlay per host. Every host stone is referenced by its id
(blockus:block/limestone) and none of its pixels ship: the stone's mod draws it.

Loot
----
Transformed from the ore's own tables, never written by hand: the silk-touch branch drops our block,
everything else is the ore's. One set per era, because the format changed at 26.3, each in a pack
overlay folder that pack.mcmeta enables by data format, so one jar serves every 26.x version:
  era263   from the 26.3 client jar; silk touch is "condition": "minecraft:tool/can_silk_touch".
  era261   from the 26.1.2 client jar (it spells out defaults 26.2 leaves implicit, and loads on
           both); silk touch is a minecraft:match_tool condition.
  mc26.1, mc26.2   a table an ore mod changed between its 26.1.2 and 26.2 builds, one per version.
A modded ore's tables come from its own mod's jar, one per era it exists in (MOD_JARS); an ore with
no 26.3 release (zinc, Mythic Metals, ...) has none in era263.
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
# Seamless Ores' 26.x textures: every modded overlay under its unique key (<key>_overlay.png).
SO_TEXTURES = os.environ.get("SO_TEXTURES", os.path.join(
    os.path.dirname(ROOT), "seamlessores-26.1.X-multiloader", "common", "src", "main", "resources", "assets",
    "seamlessores", "textures", "block"))
MODDED_PAIRS = os.path.join(ROOT, "tools", "modded_pairs.json")
CONTENT_JAVA = os.path.join(ROOT, "common", "src", "main", "java", "com", "chillpavz", MOD_ID, "content")
FABRIC_PACKS = os.path.join(ROOT, "fabric", "src", "main", "resources", "resourcepacks")
NEOFORGE_DATA = os.path.join(ROOT, "neoforge", "src", "main", "resources", "data")

# Each ore mod's jar per era, in references/jars: loot tables, tool tiers and c:ores tags come from it.
# era261 serves 26.1.x and 26.2 and reads a 26.1.2 jar where the mod has one (the format 26.2 also
# loads); a mod that exists only at 26.2 is read from its 26.2 jar. No 263 entry: no 26.3 release.
# A "262" entry is the mod's 26.2 jar where it also has a 26.1.2 one: a table that differs between the
# two goes to the mc26.1 and mc26.2 overlays instead of era261, so each version drops what its own mod does.
MOD_JARS = {
    "create": {"261": "26.1.2-create-fly-26.1.2-6.0.9-4.jar"},
    "energizedpower": {"261": "26.1.2-energizedpower-3.0.0+26.1.x-neoforge.jar",
                       "262": "energizedpower-3.0.0+26.2.x-neoforge.jar",
                       "263": "energizedpower-3.0.1+26.3.x-neoforge.jar"},
    "mysticalagriculture": {"261": "MysticalAgriculture-26.1.2-9.0.9.jar"},
    "mythicmetals": {"261": "26.1.2-mythicmetals-0.26.0+26.1.2.jar"},
    "mythicupgrades": {"261": "mythicupgrades-fabric-26.2-5.1.1.jar", "263": "mythicupgrades-fabric-26.3-5.1.1.jar"},
    "occultism": {"261": "occultism-26.1.2-neoforge-1.251.0.jar", "262": "occultism-26.2-neoforge-1.253.1.jar",
                  "263": "occultism-26.3-neoforge-1.256.0.jar"},
    "powah": {"261": "26.1.2-Powah-7.0.4-alpha.jar"},
    "silentgear": {"261": "silent-gear-26.1.2-neoforge-4.2.2.jar"},
    "silentgems": {"261": "silentgems-26.1.2-neoforge-5.1.4.jar"},
    "techreborn": {"261": "26.1.x-TechReborn-6.0.5.jar", "262": "26.2-TechReborn-6.1.1.jar",
                   "263": "26.3-TechReborn-6.2.0.jar"},
}
# A translucent ore (Silent's Gems' opal) cannot share one overlay: ours render cutout, so each host
# takes one precomposited onto that rock, made by the pack's solve_translucent_ore.py.
HOST_OVERLAYS = {("opal", "forbidden_arcanus:darkstone"):
                 ("opal_darkstone", "silent gems/opal_extracted/darkstone_opal_overlay.png")}
OVERLAYS = os.environ.get("OVERLAYS", os.path.join(
    os.path.dirname(ROOT), "seamless-glowing-ores", "assets", "overlays"))

# Every ore kind, in OreKind order. mod: the ore's own mod (None for vanilla); forms: the ore blocks,
# stone form first; loot: where its tables come from; overlay: the art, relative to OVERLAYS; tag: the
# c:ores/<tag> it belongs in; name: how it reads in a block name.
# The modded ones follow from tools/modded_pairs.json, in its order, which is the OreKind order.
ORES = {
    "coal": {}, "iron": {}, "copper": {}, "gold": {}, "redstone": {}, "emerald": {},
    "lapis": {"name": "Lapis Lazuli"}, "diamond": {},
    "zinc": {"mod": "create", "forms": ["create:zinc_ore", "create:deepslate_zinc_ore"],
             "overlay": "create/zinc_overlay.png"},
    "nether_gold": {"forms": ["minecraft:nether_gold_ore"], "tag": "gold"},
    "quartz": {"forms": ["minecraft:nether_quartz_ore"], "name": "Nether Quartz"},
}
# Words that do not title-case into the right name.
WORDS = {"techreborn": "Tech Reborn", "silents": "Silent's"}
MODDED = json.load(open(MODDED_PAIRS, encoding="utf-8"))
for _ore, _kind in MODDED["kinds"].items():
    if _ore in ORES:
        sys.exit(f"{_ore}: a modded kind reuses a hand-written ore's id")
    ORES[_ore] = {"mod": _kind["mod"], "forms": _kind["forms"], "overlay": None, "kind": _kind,
                  "name": " ".join(WORDS.get(w, w.capitalize()) for w in _ore.split("_"))}
for _ore, _info in ORES.items():
    _info.setdefault("mod", None)
    _info.setdefault("forms", [f"minecraft:{_ore}_ore", f"minecraft:deepslate_{_ore}_ore"])
    _info.setdefault("overlay", f"vanilla/{_ore}_overlay.png")
    _info.setdefault("tag", _ore)
    _info.setdefault("name", " ".join(w.capitalize() for w in _ore.split("_")))

TOOL_TAGS = ["needs_stone_tool", "needs_iron_tool", "needs_diamond_tool"]
FACES = ["down", "up", "north", "south", "west", "east"]

# Display names of the mods that place the hosts, for the config screen and the README.
MOD_NAMES = {"blockus": "Blockus", "create": "Create", "forbidden_arcanus": "Forbidden and Arcanus",
             "mythicupgrades": "Mythic Upgrades", "promenade": "Promenade", "wilderwild": "Wilder Wild"}
# The ore mods: display name, author and licence, as Seamless Ores credits them (read from each jar).
ORE_MODS = {
    "create": ("Create", "", "MIT"),
    "energizedpower": ("Energized Power", "JDDev0", "MIT"),
    "mysticalagriculture": ("Mystical Agriculture", "BlakeBr0", "MIT"),
    "mythicmetals": ("Mythic Metals", "Noaaan", "MIT"),
    "mythicupgrades": ("Mythic Upgrades", "TriQue", "MIT"),
    "occultism": ("Occultism", "Kli Kli", "MIT"),
    "powah": ("Powah", "owmii, Technici4n, shartte", "LGPL-3.0"),
    "silentgear": ("Silent Gear", "SilentChaos512", "MIT"),
    "silentgems": ("Silent's Gems", "SilentChaos512", "MIT"),
    "techreborn": ("Tech Reborn", "Team Reborn, modmuss50, drcrazy", "MIT"),
}
# Where each of those mods exists at 26.x, measured with references/tools/som-grid/availability.py.
MOD_BANDS = {"blockus": "Fabric, 26.1.x to 26.3", "create": "Create Fly, Fabric, 26.1.2 and 26.2",
             "forbidden_arcanus": "NeoForge, 26.1.2", "mythicupgrades": "Fabric and NeoForge, 26.2 and 26.3",
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
    "mythicupgrades:sapphire_schist": ("mythicupgrades:block/sapphire_schist", "single"),
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
                         r'EnumSet\.(?:of\(([^)]*)\)|noneOf\(OreKind\.class\))\)(\s*\.placedBy\("(\w+)"\))?\s*;', re.S)
    hosts = []
    for ns, path, strength, ores, _p, placed in pattern.findall(text):
        listed = [o.strip().lower() for o in ores.split(",") if o.strip()]
        unknown = [o for o in listed if o not in ORES or "kind" in ORES[o]]
        if unknown:
            sys.exit(f"{ns}:{path} lists unknown ores {unknown}")
        listed += list(MODDED["hosts"].get(f"{ns}:{path}", {}))
        hosts.append((ns, path, placed or ns, strength.lower(), [o for o in ORES if o in listed]))
    missing = set(MODDED["hosts"]) - {f"{h[0]}:{h[1]}" for h in hosts}
    if missing:
        sys.exit(f"tools/modded_pairs.json has pairs for hosts not in the table: {sorted(missing)}")
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


def is_silk_touch_branch(node):
    """Whether this entry or pool carries a Silk Touch condition (not an inverted one)."""
    condition = node.get("condition")
    if isinstance(condition, str):
        return condition.endswith("can_silk_touch")
    if isinstance(condition, dict):
        return condition.get("type") == "minecraft:match_tool" and "silk_touch" in json.dumps(condition)
    return any(c.get("condition") == "minecraft:match_tool" and "silk_touch" in json.dumps(c)
               for c in node.get("conditions", []))


def swap_silk_drops(table, source, ours):
    """Point every drop of the ore's own block that Silk Touch guards at our block instead.

    The guard sits on the entry in vanilla's tables (an alternatives child) and on the whole pool in
    Tech Reborn's. Returns how many drops were swapped.
    """
    swapped = 0

    def visit(entry, guarded):
        nonlocal swapped
        guarded = guarded or is_silk_touch_branch(entry)
        if guarded and entry.get("name") == source:
            entry["name"] = ours
            swapped += 1
        for child in entry.get("children", []):
            visit(child, guarded)

    for pool in table.get("pools", []):
        for entry in pool.get("entries", []):
            visit(entry, is_silk_touch_branch(pool))
    return swapped


def stone_name(path):
    return STONE_NAMES.get(path) or " ".join(w.capitalize() for w in path.split("_"))


def camel(*parts):
    words = "_".join(parts).split("_")
    return words[0] + "".join(w[:1].upper() + w[1:] for w in words[1:])


def ore_source(ore, strength):
    """The ore block whose loot and tool tier a variant takes: the deepslate form for a deepslate host."""
    forms = ORES[ore]["forms"]
    return forms[1] if strength == "deepslate" and len(forms) > 1 else forms[0]


def mod_jar(mod, era):
    """The ore mod's jar for this era, or None where it has no release in that era."""
    name = MOD_JARS[mod].get(era)
    return zipfile.ZipFile(os.path.join(JARS, name)) if name else None


def newest_jar(mod):
    return mod_jar(mod, "263") or mod_jar(mod, "261")


def loot_table(jars, era, ore, strength):
    """The ore's own table for this era, or None if the ore has none in that era."""
    ns, name = ore_source(ore, strength).split(":")
    mod = ORES[ore]["mod"]
    jar = jars[era] if mod is None else jars.get((mod, era))
    if jar is None:
        return None
    path = f"data/{ns}/loot_table/blocks/{name}.json"
    if path not in jar.namelist():
        sys.exit(f"{os.path.basename(jar.filename)} has no {path}")
    return json.load(jar.open(path))


def overlay_of(ore, host, strength):
    """(texture name, source file) of the overlay a variant wears."""
    if (ore, host) in HOST_OVERLAYS:
        key, rel = HOST_OVERLAYS[(ore, host)]
        return key, os.path.join(OVERLAYS, rel)
    kind = ORES[ore].get("kind")
    if kind is None:
        return ore, os.path.join(OVERLAYS, ORES[ore]["overlay"])
    key = kind["deepslate_overlay"] if strength == "deepslate" and kind["deepslate_overlay"] else ore
    return key, os.path.join(SO_TEXTURES, f"{key}_overlay.png")


def jar_tags(jar, kind):
    """tag id -> members of every tag of this kind in the jar, nested references resolved."""
    tags = {}
    for n in jar.namelist():
        m = re.match(rf"^data/([^/]+)/tags/{kind}s?/(.+)\.json$", n)
        if m:
            try:
                values = json.loads(jar.read(n)).get("values", [])
            except ValueError:
                continue
            tags[f"{m[1]}:{m[2]}"] = [v["id"] if isinstance(v, dict) else v for v in values]

    def resolve(tag, seen):
        out = set()
        for v in tags.get(tag, []):
            if v.startswith("#"):
                if v[1:] not in seen:
                    out |= resolve(v[1:], seen | {v[1:]})
            else:
                out.add(v)
        return out
    return {t: resolve(t, {t}) for t in tags}


def normalised(table):
    """A table with the defaults one format spells out and the other leaves implicit removed."""
    if isinstance(table, dict):
        return {k: normalised(v) for k, v in table.items() if k != "bonus_rolls"}
    if isinstance(table, list):
        return [normalised(v) for v in table]
    if isinstance(table, float) and table == int(table):
        return int(table)
    return table


def write_loot(table, source_id, our_id, name, gate, folders, era):
    """The ore's own table with its Silk Touch drop pointed at our block, gated on our block existing."""
    silk = swap_silk_drops(table, source_id, our_id)
    # An ore that always drops itself (Tech Reborn 6.0.5's bauxite) has no silk branch: our variant then
    # drops that mod's own ore, the item every recipe for it expects, as Seamless Ores' variants do.
    # Anything else is a table shape nobody has checked.
    drops_itself = f'"name": "{source_id}"' in json.dumps(table)
    if silk != 1 and not (silk == 0 and drops_itself):
        sys.exit(f"{source_id} ({era}): expected one silk touch drop of the ore, found {silk}")
    table["random_sequence"] = f"{MOD_ID}:blocks/{name}"
    table = {
        "fabric:load_conditions": [{"condition": "fabric:registry_contains",
                                    "registry": "minecraft:block", "values": [our_id]}],
        "neoforge:conditions": [{"type": "neoforge:mod_loaded", "modid": m} for m in gate],
        **table,
    }
    for folder in folders:
        write_json(os.path.join(folder, MOD_ID, "loot_table", "blocks", f"{name}.json"), table)


def main():
    hosts = read_hosts()
    for ns, path, *_rest in hosts:
        if f"{ns}:{path}" not in HOST_LOOK:
            sys.exit(f"{ns}:{path} has no HOST_LOOK entry")
    for jar in list(ERAS.values()) + [os.path.join(JARS, n) for m in MOD_JARS.values() for n in m.values()]:
        if not os.path.exists(jar):
            sys.exit(f"jar not found: {jar}")
    for ore, info in ORES.items():
        if info["mod"] and info["mod"] not in MOD_JARS:
            sys.exit(f"{ore}: no MOD_JARS entry for {info['mod']}")
    paths = [path for _ns, path, *_r in hosts]
    clashes = {p for p in paths if paths.count(p) > 1}

    assets = os.path.join(COMMON, "assets", MOD_ID)
    data = os.path.join(COMMON, "data")
    # Pack overlay folders, named in pack.mcmeta with the data formats each serves.
    era_data = {era: os.path.join(COMMON, f"era{era}", "data") for era in ERAS}
    global MC_DATA
    MC_DATA = {"26.1.2": os.path.join(COMMON, "mc26.1", "data"), "26.2": os.path.join(COMMON, "mc26.2", "data")}
    split = []
    # Generated folders are rebuilt from scratch, so a host or ore taken out of the table leaves no file.
    for sub in ("blockstates", "models", "items", "textures"):
        shutil.rmtree(os.path.join(assets, sub), ignore_errors=True)
    for sub in ("c", "minecraft"):
        shutil.rmtree(os.path.join(data, sub), ignore_errors=True)
    for root in list(era_data.values()) + list(MC_DATA.values()):
        shutil.rmtree(os.path.join(root, MOD_ID, "loot_table"), ignore_errors=True)
    shutil.rmtree(FABRIC_PACKS, ignore_errors=True)
    shutil.rmtree(NEOFORGE_DATA, ignore_errors=True)

    lang = {f"itemGroup.{MOD_ID}.ores": "Seamless Ores: Matrix"}
    mineable, tool_tags, foreign_tool_tags, conv, conv_modded = [], {}, {}, {}, {}
    overlays = {}           # texture name -> source file
    count = 0

    jars = {era: zipfile.ZipFile(path) for era, path in ERAS.items()}
    for mod in MOD_JARS:
        for era in list(ERAS) + ["262"]:
            jars[(mod, era)] = mod_jar(mod, era)
    # Tool tiers from the ore's own mod: vanilla's tags for a vanilla ore, the mod's newest jar for its
    # own. A mod may also gate its ores with tags in its own namespace that feed vanilla's
    # incorrect_for_<tool> lists (Mythic Metals' needs_copper_tools and needs_netherite_tool): a variant
    # left out of them would mine a tier too cheaply, so their membership is mirrored too.
    tool_members = {tag: set(json.load(jars["263"].open(f"data/minecraft/tags/block/{tag}.json"))["values"])
                    for tag in TOOL_TAGS}
    own_tool_tags, ore_tags = {}, {}
    for mod in MOD_JARS:
        jar = newest_jar(mod)
        blocks = jar_tags(jar, "block")
        for tag, members in blocks.items():
            ns, tpath = tag.split(":", 1)
            if ns == "minecraft" and tpath in TOOL_TAGS:
                tool_members[tpath] |= members
            elif ns != "minecraft" and re.fullmatch(r"needs_[a-z_]+", tpath):
                own_tool_tags.setdefault(tag, set()).update(members)
        # c:ores/<material> parity: every such tag the ore we stand in for is in, read from its jar.
        for kind in ("block", "item"):
            for tag, members in jar_tags(jar, kind).items():
                if tag.startswith("c:ores/"):
                    for member in members:
                        ore_tags.setdefault((kind, member), set()).add(tag[len("c:ores/"):])

    for ns, path, placer, strength, kinds in hosts:
        stone, look = HOST_LOOK[f"{ns}:{path}"]
        for ore in kinds:
            info = ORES[ore]
            name = f"{ns}_{path}_{ore}_ore"
            our_id = f"{MOD_ID}:{name}"
            base = f"{MOD_ID}:block/{name}"
            texture, source = overlay_of(ore, f"{ns}:{path}", strength)
            overlays[texture] = source

            models = os.path.join(assets, "models", "block")
            if look == "single":
                state = {"variants": {"": {"model": base}}}
                write_json(os.path.join(models, f"{name}.json"), model(stone, texture))
            elif look == "mirrored_turned":
                state = {"variants": {"": [{"model": base}, {"model": base + "_mirrored"},
                                           {"model": base, "y": 180}, {"model": base + "_mirrored", "y": 180}]}}
                write_json(os.path.join(models, f"{name}.json"), model(stone, texture))
                write_json(os.path.join(models, f"{name}_mirrored.json"), model(stone, texture, True))
            elif look == "textures4":
                # Create picks one of four natural textures per block; ours picks the same way, so a
                # vein does not show as the one repeated tile in a varied wall.
                state = {"variants": {"": [{"model": f"{base}_{i}"} for i in range(4)]}}
                for i in range(4):
                    write_json(os.path.join(models, f"{name}_{i}.json"), model(f"{stone}{i}", texture))
                # The item needs one model to point at.
                write_json(os.path.join(models, f"{name}.json"), model(f"{stone}0", texture))
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
            source_id = ore_source(ore, strength)
            for era in ERAS:
                table = loot_table(jars, era, ore, strength)
                if table is None:
                    continue
                targets = [era_data[era]]
                if era == "261" and info["mod"] and jars.get((info["mod"], "262")):
                    newer = loot_table(jars, "262", ore, strength)
                    if normalised(newer) != normalised(table):
                        write_loot(newer, source_id, our_id, name, gate, [MC_DATA["26.2"]], era)
                        targets = [MC_DATA["26.1.2"]]
                        split.append(name)
                write_loot(table, source_id, our_id, name, gate, targets, era)


            # Optional entries: a variant only exists when its mods are installed, and a required entry
            # naming an absent block fails the whole tag.
            entry = {"id": our_id, "required": False}
            mineable.append(entry)
            for tag, members in tool_members.items():
                if source_id in members:
                    tool_tags.setdefault(tag, []).append(entry)
            for tag, members in own_tool_tags.items():
                if source_id in members:
                    foreign_tool_tags.setdefault(tag, []).append(entry)
            if info["mod"] is None:
                conv.setdefault(info["tag"], []).append(entry)
            else:
                for kind in ("block", "item"):
                    materials = ore_tags.get((kind, source_id), set()) | ({info["tag"]} if ore == "zinc" else set())
                    # Parity: an ore its own mod keeps out of every c:ores/<material> tag stays out of
                    # them here too, and is still in c:ores itself.
                    for material in sorted(materials):
                        conv_modded.setdefault((info["mod"], kind, material), []).append(entry)
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
            f" its own look. Applies to newly generated chunks, from the next world load.")

    lang = dict(sorted(lang.items()))
    for key, value in lang.items():
        if any(ch in value for ch in (chr(0x2013), chr(0x2014))):
            sys.exit(f"dash in public text: {key}")
    write_json(os.path.join(assets, "lang", "en_us.json"), lang)

    textures = os.path.join(assets, "textures", "block")
    os.makedirs(textures, exist_ok=True)
    for texture, source in sorted(overlays.items()):
        if not os.path.exists(source):
            sys.exit(f"overlay missing: {source}")
        shutil.copyfile(source, os.path.join(textures, f"{texture}_overlay.png"))

    write_json(os.path.join(data, "minecraft", "tags", "block", "mineable", "pickaxe.json"), {"values": mineable})
    for tag, values in tool_tags.items():
        write_json(os.path.join(data, "minecraft", "tags", "block", f"{tag}.json"), {"values": values})
    # A mod's own tier tags merge with that mod's file; every entry is optional, so the file is inert
    # without the mod.
    for tag, values in foreign_tool_tags.items():
        ns, tpath = tag.split(":", 1)
        write_json(os.path.join(data, ns, "tags", "block", f"{tpath}.json"), {"values": values})
    everything = sorted(mineable, key=lambda e: e["id"])
    for kind in ("block", "item"):
        write_json(os.path.join(data, "c", "tags", kind, "ores.json"), {"values": everything})
        for tag, values in conv.items():
            write_json(os.path.join(data, "c", "tags", kind, "ores", f"{tag}.json"), {"values": values})
    write_modded_material_tags(conv_modded)

    write_java(hosts)
    write_config(hosts)
    write_readme(hosts, count, sorted(overlays), clashes)

    per_mod = {}
    for _ns, _path, placer, _s, kinds in hosts:
        per_mod[placer] = per_mod.get(placer, 0) + len(kinds)
    print(f"{count} variants ({', '.join(f'{m} {n}' for m, n in per_mod.items())}); "
          f"{len(overlays)} overlays; loot eras {', '.join(ERAS)}; per-version loot for {len(split)} variants")


def write_modded_material_tags(conv_modded):
    """c:ores/<material> for a modded ore's variants: never in a Fabric world without that ore's mod.

    FABRIC'S tags_populated CONDITION ASKS WHETHER A TAG EXISTS, NOT WHETHER ANYTHING IS IN IT. A
    c:ores/tin file whose only entries are optional variants would therefore "populate" c:ores/tin in
    a world without any tin mod, recipes gated on it load with an ingredient that matches nothing, and
    some mods crash on that (Seamless Ores hit it with Alloy Forgery). Fabric applies no conditions to
    tag files, so on Fabric each ore mod's entries go in a built-in data pack of their own
    (fabric/.../resourcepacks/<mod>/), which SeamlessOresMatrixFabric registers only when that mod is
    loaded. NeoForge gets plain files in its own module.
    """
    for (mod, kind, material), values in sorted(conv_modded.items()):
        rel = os.path.join("tags", kind, "ores", f"{material}.json")
        write_json(os.path.join(FABRIC_PACKS, mod, "data", "c", rel), {"values": values})
        write_json(os.path.join(NEOFORGE_DATA, "c", rel), {"values": sorted(
            values + json.load(open(os.path.join(NEOFORGE_DATA, "c", rel)))["values"]
            if os.path.exists(os.path.join(NEOFORGE_DATA, "c", rel)) else values, key=lambda e: e["id"])})


def java_xp(xp):
    if xp is None:
        return "null"
    lo, hi = xp
    return f"ConstantInt.of({lo})" if lo == hi else f"UniformInt.of({lo}, {hi})"


def write_java(hosts):
    """The modded OreKind constants, and ModdedPairs: which modded kinds each host takes."""
    lines = []
    modded = [o for o in ORES if "kind" in ORES[o]]
    for ore in modded:
        k = ORES[ore]["kind"]
        strength = "null" if not k["strength"] else \
            "new float[] {" + ", ".join(f"{v:.1f}F" for v in k["strength"]) + "}"
        forms = ", ".join(f'"{f}"' for f in k["forms"])
        lines.append(f'    {ore.upper()}("{ore}", "{k["mod"]}", "{k["seamless_ores_name"]}", {str(k["nether"]).lower()},')
        lines.append(f'            {java_xp(k["xp"])}, {java_xp(k["deepslate_xp"])}, {strength},')
        lines.append(f'            {forms}),')
    path = os.path.join(CONTENT_JAVA, "OreKind.java")
    text = open(path, encoding="utf-8").read()
    # Every constant, hand-written or generated, ends with a comma; the enum's own ";" follows the block.
    text = replace_block(text, "    // BEGIN GENERATED modded kinds (tools/generate_assets.py, from tools/modded_pairs.json)\n",
                         "    // END GENERATED modded kinds", "\n".join(lines) + "\n" if lines else "", path)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)

    cases = []
    for host, pairs in MODDED["hosts"].items():
        listed = [o for o in ORES if o in pairs]
        cases.append(f'            case "{host}" -> EnumSet.of({", ".join("OreKind." + o.upper() for o in listed)});')
    java = f"""package com.chillpavz.{MOD_ID}.content;

import java.util.EnumSet;
import java.util.Set;

/**
 * Which other mods' ores each host swallows, as measured by the pair model: every ore that reaches the
 * stone at a rate above the floor, in a band and on a loader where both mods exist.
 *
 * <p>GENERATED by tools/generate_assets.py from tools/modded_pairs.json. Do not edit.
 */
final class ModdedPairs {{

    private ModdedPairs() {{}}

    /** The modded kinds the host with this id takes; none for a host with no modded pairs. */
    static Set<OreKind> of(String host) {{
        return switch (host) {{
{chr(10).join(cases)}
            default -> EnumSet.noneOf(OreKind.class);
        }};
    }}
}}
"""
    with open(os.path.join(CONTENT_JAVA, "ModdedPairs.java"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(java)


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
             f"its stone is installed, and one of another mod's ore only with that mod as well. A block's id "
             f"is `<stone>_<ore>_ore`, from the two columns below: `blockus_limestone` and `iron` make "
             f"`blockus_limestone_iron_ore`.", ""]
    for placer in dict.fromkeys(h[2] for h in hosts):
        stones = [(ns, p, k) for ns, p, pl, _s, k in hosts if pl == placer]
        lines.append(f"**{MOD_NAMES[placer]}, requires `{placer}`** ({MOD_BANDS[placer]})")
        lines.append("")
        lines.append("Stones: " + ", ".join(f"{stone_name(p)} `{ns}_{p}`" for ns, p, _k in stones))
        lines.append("")
        lines.append("| Ore | `<ore>` | Also requires | In |")
        lines.append("|---|---|---|---|")
        for ore in ORES:
            within = [stone_name(p) for _ns, p, k in stones if ore in k]
            if not within:
                continue
            mod = ORES[ore]["mod"]
            needs = f"{ORE_MODS[mod][0]} `{mod}`" if mod and mod != placer else ""
            where = "every stone" if len(within) == len(stones) and len(stones) > 1 else ", ".join(within)
            lines.append(f"| {ORES[ore]['name']} | `{ore}` | {needs} | {where} |")
        lines.append("")
    text = replace_section(text, "block-list", "\n".join(lines).rstrip())

    used = {ORES[o]["mod"] for h in hosts for o in h[4]} - {None}
    credits = ["The vanilla ore overlays are derived from Minecraft's own textures and remain Mojang's",
               "property. Each other mod's overlay is derived from that mod's own ore texture, so it is",
               "theirs and is used under the licence shown:", "",
               "| Mod | Author | Licence |", "|---|---|---|"]
    # A bare "-" for an unstated author: a not-applicable marker inside a table is the one allowed dash.
    credits += [f"| {n} | {a or '-'} | {l} |" for m, (n, a, l) in sorted(ORE_MODS.items(), key=lambda i: i[1][0])
                if m in used]
    credits += ["", "No texture from any stone mod ships in this jar; each stone is referenced by its id."]
    text = replace_section(text, "credits", "\n".join(credits))

    listed = " ".join(f"`{o}`" for o in overlays)
    fence = "```"
    text = replace_section(text, "overlay-list", (
        f"Every variant of one ore shares a single overlay texture, so covering all {count} blocks "
        f"takes **{len(overlays)} PNG files**:\n\n{fence}\nassets/{MOD_ID}/textures/block/<ore>_overlay.png\n"
        f"{fence}\n\nwhere `<ore>` is one of: {listed}\n\n"
        f"Two keys are not an ore id. `unobtainium_deepslate` is Mythic Metals' deepslate look, worn in "
        f"the stones as hard as deepslate. `opal_darkstone` is opal painted onto darkstone: opal is "
        f"translucent, so each rock takes its own precomposited overlay."))

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
