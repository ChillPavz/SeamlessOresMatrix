# Seamless Ores: Matrix

Ore blocks that match the modded stone they generate in. When a stone from another mod forms around
ore, the ore normally keeps its plain stone or deepslate look and shows up as a square of the wrong
rock. Matrix gives that ore the stone it actually sits in.

**It adds no ore.** The same veins, in the same places and the same amounts, drawn to fit their
surroundings.

| | |
|---|---|
| Minecraft | 26.3 |
| Loaders | Fabric, NeoForge |
| Requires | Cloth Config. On Fabric, Mod Menu is optional and adds the config button |
| Licence | PolyForm Shield 1.0.0, see `LICENSE` |

An original mod. Not a fork or a port of any other project.

## How it fits with Seamless Ores

[Seamless Ores](https://modrinth.com/mod/seamless-ores) covers the vanilla stones: granite, diorite,
andesite, tuff, basalt and blackstone. Matrix covers stones that other mods add. The two work alone
or together, and nothing is covered twice.

- Mining, drops, Fortune, Silk Touch and experience match the vanilla ore.
- Every overlay is hand drawn and shared with Seamless Ores. The stone itself is drawn by the mod
  that adds it, so a resource pack that retextures that stone restyles these ores too.
- A variant only exists when its stone's mod is installed. With no supported stone mod, Matrix does
  nothing at all.

## Companion resource pack

[Seamless Glowing Ores](https://modrinth.com/resourcepack/seamless-glowing-ores) makes every ore
glow, with an optional connected outline that joins touching ore of the same type across different
host stones. It covers Matrix's blocks as well as Seamless Ores'.

## Block list

<!-- BEGIN GENERATED block-list -->
**36 blocks** in the `seamlessoresmatrix` namespace. Each exists only when its stone's mod is installed.

**Blockus, requires `blockus`**

| | limestone | marble | bluestone | viridite |
|---|---|---|---|---|
| Coal | `blockus_limestone_coal_ore` | `blockus_marble_coal_ore` | `blockus_bluestone_coal_ore` |  |
| Iron | `blockus_limestone_iron_ore` | `blockus_marble_iron_ore` | `blockus_bluestone_iron_ore` | `blockus_viridite_iron_ore` |
| Copper | `blockus_limestone_copper_ore` | `blockus_marble_copper_ore` | `blockus_bluestone_copper_ore` |  |
| Gold | `blockus_limestone_gold_ore` | `blockus_marble_gold_ore` | `blockus_bluestone_gold_ore` | `blockus_viridite_gold_ore` |
| Redstone | `blockus_limestone_redstone_ore` | `blockus_marble_redstone_ore` | `blockus_bluestone_redstone_ore` | `blockus_viridite_redstone_ore` |
| Emerald | `blockus_limestone_emerald_ore` | `blockus_marble_emerald_ore` | `blockus_bluestone_emerald_ore` |  |
| Lapis Lazuli | `blockus_limestone_lapis_ore` | `blockus_marble_lapis_ore` | `blockus_bluestone_lapis_ore` | `blockus_viridite_lapis_ore` |
| Diamond | `blockus_limestone_diamond_ore` | `blockus_marble_diamond_ore` | `blockus_bluestone_diamond_ore` | `blockus_viridite_diamond_ore` |

**Wilder Wild, requires `wilderwild`**

| | gabbro |
|---|---|
| Coal | `wilderwild_gabbro_coal_ore` |
| Iron | `wilderwild_gabbro_iron_ore` |
| Copper | `wilderwild_gabbro_copper_ore` |
| Gold | `wilderwild_gabbro_gold_ore` |
| Redstone | `wilderwild_gabbro_redstone_ore` |
| Lapis Lazuli | `wilderwild_gabbro_lapis_ore` |
| Diamond | `wilderwild_gabbro_diamond_ore` |
<!-- END GENERATED block-list -->

## Configuration

One switch per stone, grouped by the mod that adds it; a group is hidden when its mod is not
installed. Every switch gates **worldgen only, never registration**, so a client and a server cannot
disagree about which blocks exist. Turning a stone off means its ore keeps the vanilla look in newly
generated chunks. The blocks still exist, and chunks that already generated never change.

Settings take effect the next time a world is loaded.

## For resource pack authors

<!-- BEGIN GENERATED overlay-list -->
Every variant of one ore shares a single overlay texture, so covering all 36 blocks takes **8 PNG files**:

```
assets/seamlessoresmatrix/textures/block/<ore>_overlay.png
```

where `<ore>` is one of: `coal` `copper` `diamond` `emerald` `gold` `iron` `lapis` `redstone`
<!-- END GENERATED overlay-list -->

Each file is the ore layer only, blobs on transparency. The host stone is referenced straight from
its own mod, so you do not supply it.

## Building

Requires JDK 25.

```
./gradlew build
```

Jars land in `fabric/build/libs` and `neoforge/build/libs`. Take the plain jar, not the `-sources` or
`-javadoc` one.

Blockstates, models, lang, loot tables, tags and this README's block list are generated from the
host table in `common/.../content/HostStone.java`:

```
python tools/generate_assets.py
```

## Project layout

| Path | What it holds |
|---|---|
| `common/` | Everything shared: the host table, content registration, worldgen, config holder |
| `fabric/`, `neoforge/` | Loader entry points, the Cloth Config data class and screen |
| `tools/generate_assets.py` | Generates assets, data and the block list above |

The Cloth Config classes are duplicated across both loader modules on purpose and must stay
identical. They cannot live in `common`, because loader dependencies are not on its classpath.

## Credits

The ore overlays are derived from Minecraft's own textures and remain Mojang's property. No texture
from any stone mod ships in this jar; each stone is referenced by its id.

Built on [MultiLoader Template](https://github.com/jaredlll08/MultiLoader-Template) by jaredlll08.
