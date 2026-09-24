# Seamless Ores: Matrix

Ore blocks that match the modded stone they generate in. When a stone from another mod forms around
ore, the ore normally keeps its plain stone or deepslate look and shows up as a square of the wrong
rock. Matrix gives that ore the stone it actually sits in.

**It adds no ore.** The same veins, in the same places and the same amounts, drawn to fit their
surroundings.

| | |
|---|---|
| Minecraft | 26.1.x, 26.2, 26.3 (one jar per version) |
| Loaders | Fabric, NeoForge |
| Requires | Cloth Config. On Fabric, Mod Menu is optional and adds the config button |
| Licence | PolyForm Shield 1.0.0, see `LICENSE` |

An original mod. Not a fork or a port of any other project.

## How it fits with Seamless Ores

[Seamless Ores](https://modrinth.com/mod/seamless-ores) covers the vanilla stones: granite, diorite,
andesite, tuff, basalt and blackstone. Matrix covers stones that other mods add, and the calcite,
dripstone and smooth basalt that Create lays down in its stone strata. The two work alone or
together, and nothing is covered twice.

- Mining, drops, Fortune, Silk Touch and experience match the ore it replaces: the vanilla ore, or
  Create's own zinc ore.
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
**179 blocks** in the `seamlessoresmatrix` namespace. Each exists only when the mod that places its stone is installed, and a zinc one only with Create as well.

**Blockus, requires `blockus`** (Fabric, 26.1.x to 26.3)

| | Limestone | Marble | Bluestone | Viridite |
|---|---|---|---|---|
| Coal | `blockus_limestone_coal_ore` | `blockus_marble_coal_ore` | `blockus_bluestone_coal_ore` |  |
| Iron | `blockus_limestone_iron_ore` | `blockus_marble_iron_ore` | `blockus_bluestone_iron_ore` | `blockus_viridite_iron_ore` |
| Copper | `blockus_limestone_copper_ore` | `blockus_marble_copper_ore` | `blockus_bluestone_copper_ore` |  |
| Gold | `blockus_limestone_gold_ore` | `blockus_marble_gold_ore` | `blockus_bluestone_gold_ore` | `blockus_viridite_gold_ore` |
| Redstone | `blockus_limestone_redstone_ore` | `blockus_marble_redstone_ore` | `blockus_bluestone_redstone_ore` | `blockus_viridite_redstone_ore` |
| Emerald | `blockus_limestone_emerald_ore` | `blockus_marble_emerald_ore` | `blockus_bluestone_emerald_ore` |  |
| Lapis Lazuli | `blockus_limestone_lapis_ore` | `blockus_marble_lapis_ore` | `blockus_bluestone_lapis_ore` | `blockus_viridite_lapis_ore` |
| Diamond | `blockus_limestone_diamond_ore` | `blockus_marble_diamond_ore` | `blockus_bluestone_diamond_ore` | `blockus_viridite_diamond_ore` |
| Zinc | `blockus_limestone_zinc_ore` | `blockus_marble_zinc_ore` | `blockus_bluestone_zinc_ore` | `blockus_viridite_zinc_ore` |

**Create, requires `create`** (Create Fly, Fabric, 26.1.2 and 26.2)

| | Asurine | Crimsite | Limestone | Ochrum | Scorchia | Scoria | Veridium | Calcite | Dripstone | Smooth Basalt |
|---|---|---|---|---|---|---|---|---|---|---|
| Coal | `create_asurine_coal_ore` | `create_crimsite_coal_ore` | `create_limestone_coal_ore` | `create_ochrum_coal_ore` |  | `create_scoria_coal_ore` | `create_veridium_coal_ore` | `minecraft_calcite_coal_ore` | `minecraft_dripstone_block_coal_ore` | `minecraft_smooth_basalt_coal_ore` |
| Iron | `create_asurine_iron_ore` | `create_crimsite_iron_ore` | `create_limestone_iron_ore` | `create_ochrum_iron_ore` |  | `create_scoria_iron_ore` | `create_veridium_iron_ore` | `minecraft_calcite_iron_ore` | `minecraft_dripstone_block_iron_ore` | `minecraft_smooth_basalt_iron_ore` |
| Copper | `create_asurine_copper_ore` | `create_crimsite_copper_ore` | `create_limestone_copper_ore` | `create_ochrum_copper_ore` |  | `create_scoria_copper_ore` | `create_veridium_copper_ore` | `minecraft_calcite_copper_ore` | `minecraft_dripstone_block_copper_ore` | `minecraft_smooth_basalt_copper_ore` |
| Gold | `create_asurine_gold_ore` | `create_crimsite_gold_ore` | `create_limestone_gold_ore` | `create_ochrum_gold_ore` |  | `create_scoria_gold_ore` | `create_veridium_gold_ore` | `minecraft_calcite_gold_ore` | `minecraft_dripstone_block_gold_ore` | `minecraft_smooth_basalt_gold_ore` |
| Redstone | `create_asurine_redstone_ore` | `create_crimsite_redstone_ore` | `create_limestone_redstone_ore` | `create_ochrum_redstone_ore` |  | `create_scoria_redstone_ore` | `create_veridium_redstone_ore` | `minecraft_calcite_redstone_ore` | `minecraft_dripstone_block_redstone_ore` | `minecraft_smooth_basalt_redstone_ore` |
| Emerald | `create_asurine_emerald_ore` | `create_crimsite_emerald_ore` | `create_limestone_emerald_ore` | `create_ochrum_emerald_ore` |  | `create_scoria_emerald_ore` | `create_veridium_emerald_ore` | `minecraft_calcite_emerald_ore` | `minecraft_dripstone_block_emerald_ore` | `minecraft_smooth_basalt_emerald_ore` |
| Lapis Lazuli | `create_asurine_lapis_ore` | `create_crimsite_lapis_ore` | `create_limestone_lapis_ore` | `create_ochrum_lapis_ore` |  | `create_scoria_lapis_ore` | `create_veridium_lapis_ore` | `minecraft_calcite_lapis_ore` | `minecraft_dripstone_block_lapis_ore` | `minecraft_smooth_basalt_lapis_ore` |
| Diamond | `create_asurine_diamond_ore` | `create_crimsite_diamond_ore` | `create_limestone_diamond_ore` | `create_ochrum_diamond_ore` |  | `create_scoria_diamond_ore` | `create_veridium_diamond_ore` | `minecraft_calcite_diamond_ore` | `minecraft_dripstone_block_diamond_ore` | `minecraft_smooth_basalt_diamond_ore` |
| Zinc | `create_asurine_zinc_ore` | `create_crimsite_zinc_ore` | `create_limestone_zinc_ore` | `create_ochrum_zinc_ore` |  | `create_scoria_zinc_ore` | `create_veridium_zinc_ore` | `minecraft_calcite_zinc_ore` | `minecraft_dripstone_block_zinc_ore` | `minecraft_smooth_basalt_zinc_ore` |
| Nether Gold |  |  |  |  | `create_scorchia_nether_gold_ore` | `create_scoria_nether_gold_ore` |  |  |  | `minecraft_smooth_basalt_nether_gold_ore` |
| Nether Quartz |  |  |  |  | `create_scorchia_quartz_ore` | `create_scoria_quartz_ore` |  |  |  | `minecraft_smooth_basalt_quartz_ore` |

**Forbidden and Arcanus, requires `forbidden_arcanus`** (NeoForge, 26.1.2)

| | Darkstone |
|---|---|
| Iron | `forbidden_arcanus_darkstone_iron_ore` |
| Gold | `forbidden_arcanus_darkstone_gold_ore` |
| Redstone | `forbidden_arcanus_darkstone_redstone_ore` |
| Lapis Lazuli | `forbidden_arcanus_darkstone_lapis_ore` |
| Diamond | `forbidden_arcanus_darkstone_diamond_ore` |

**Mythic Upgrades, requires `mythicupgrades`** (Fabric and NeoForge, 26.2)

| | Aquamarine Schist | Citrine Schist | Peridot Schist | Topaz Schist |
|---|---|---|---|---|
| Coal | `mythicupgrades_aquamarine_schist_coal_ore` | `mythicupgrades_citrine_schist_coal_ore` | `mythicupgrades_peridot_schist_coal_ore` | `mythicupgrades_topaz_schist_coal_ore` |
| Iron | `mythicupgrades_aquamarine_schist_iron_ore` | `mythicupgrades_citrine_schist_iron_ore` | `mythicupgrades_peridot_schist_iron_ore` | `mythicupgrades_topaz_schist_iron_ore` |
| Copper | `mythicupgrades_aquamarine_schist_copper_ore` | `mythicupgrades_citrine_schist_copper_ore` | `mythicupgrades_peridot_schist_copper_ore` | `mythicupgrades_topaz_schist_copper_ore` |
| Gold | `mythicupgrades_aquamarine_schist_gold_ore` | `mythicupgrades_citrine_schist_gold_ore` | `mythicupgrades_peridot_schist_gold_ore` | `mythicupgrades_topaz_schist_gold_ore` |
| Redstone | `mythicupgrades_aquamarine_schist_redstone_ore` | `mythicupgrades_citrine_schist_redstone_ore` | `mythicupgrades_peridot_schist_redstone_ore` | `mythicupgrades_topaz_schist_redstone_ore` |
| Lapis Lazuli | `mythicupgrades_aquamarine_schist_lapis_ore` | `mythicupgrades_citrine_schist_lapis_ore` | `mythicupgrades_peridot_schist_lapis_ore` | `mythicupgrades_topaz_schist_lapis_ore` |
| Diamond | `mythicupgrades_aquamarine_schist_diamond_ore` | `mythicupgrades_citrine_schist_diamond_ore` | `mythicupgrades_peridot_schist_diamond_ore` | `mythicupgrades_topaz_schist_diamond_ore` |

**Promenade, requires `promenade`** (Fabric, 26.1.x and 26.2)

| | Asphalt | Blunite |
|---|---|---|
| Coal | `promenade_asphalt_coal_ore` | `promenade_blunite_coal_ore` |
| Iron | `promenade_asphalt_iron_ore` | `promenade_blunite_iron_ore` |
| Copper | `promenade_asphalt_copper_ore` | `promenade_blunite_copper_ore` |
| Gold | `promenade_asphalt_gold_ore` | `promenade_blunite_gold_ore` |
| Redstone | `promenade_asphalt_redstone_ore` | `promenade_blunite_redstone_ore` |
| Emerald | `promenade_asphalt_emerald_ore` | `promenade_blunite_emerald_ore` |
| Lapis Lazuli | `promenade_asphalt_lapis_ore` | `promenade_blunite_lapis_ore` |
| Diamond | `promenade_asphalt_diamond_ore` | `promenade_blunite_diamond_ore` |
| Zinc | `promenade_asphalt_zinc_ore` | `promenade_blunite_zinc_ore` |

**Wilder Wild, requires `wilderwild`** (Fabric 26.1.x to 26.3, NeoForge 26.2 and 26.3)

| | Gabbro |
|---|---|
| Coal | `wilderwild_gabbro_coal_ore` |
| Iron | `wilderwild_gabbro_iron_ore` |
| Copper | `wilderwild_gabbro_copper_ore` |
| Gold | `wilderwild_gabbro_gold_ore` |
| Redstone | `wilderwild_gabbro_redstone_ore` |
| Lapis Lazuli | `wilderwild_gabbro_lapis_ore` |
| Diamond | `wilderwild_gabbro_diamond_ore` |
| Zinc | `wilderwild_gabbro_zinc_ore` |
<!-- END GENERATED block-list -->

## Configuration

One switch per stone, grouped by the mod that places it; a group is hidden when its mod is not
installed. Every switch gates **worldgen only, never registration**, so a client and a server cannot
disagree about which blocks exist. Turning a stone off means its ore keeps the vanilla look in newly
generated chunks. The blocks still exist, and chunks that already generated never change.

Settings take effect the next time a world is loaded.

## For resource pack authors

<!-- BEGIN GENERATED overlay-list -->
Every variant of one ore shares a single overlay texture, so covering all 179 blocks takes **11 PNG files**:

```
assets/seamlessoresmatrix/textures/block/<ore>_overlay.png
```

where `<ore>` is one of: `coal` `iron` `copper` `gold` `redstone` `emerald` `lapis` `diamond` `zinc` `nether_gold` `quartz`
<!-- END GENERATED overlay-list -->

Each file is the ore layer only, blobs on transparency. The host stone is referenced straight from
its own mod, so you do not supply it.

## Building

Requires JDK 25. One source tree builds every Minecraft version; pick it with `-Pmc`:

```
./gradlew build -Pmc=26.3
./gradlew build -Pmc=26.2
./gradlew build -Pmc=26.1.x
```

`26.3` is the default. Jars land in `fabric/build/libs` and `neoforge/build/libs`, named after the
Minecraft version (the 26.1.x jar is built against 26.1.2). Take the plain jar, not the `-sources` or
`-javadoc` one.

Blockstates, models, lang, loot tables, tags and this README's block list are generated from the
host table in `common/.../content/HostStone.java`:

```
python tools/generate_assets.py
```

It reads loot tables from the 26.3 and 26.1.2 Minecraft client jars (which a build of each version
leaves in the Gradle cache) and zinc's from a Create Fly 26.1.2 jar.

## Project layout

| Path | What it holds |
|---|---|
| `versions/` | One properties file per Minecraft version: Minecraft, loader, Cloth and Mod Menu versions |
| `common/src/main` | Everything shared: the host table, content registration, both worldgen injectors, config holder |
| `common/src/era263`, `common/src/era261` | What changed shape at 26.3: how ore features are read and rebuilt, the access widener and transformer, loot tables. `era261` serves 26.1.x and 26.2 |
| `fabric/`, `neoforge/` | Loader entry points, the Cloth Config data class and screen |
| `tools/generate_assets.py` | Generates assets, data and the block list above |

The Cloth Config classes are duplicated across both loader modules on purpose and must stay
identical. Their switches are generated from the host table. They cannot live in `common`, because loader dependencies are not on its classpath.

## Credits

The ore overlays are derived from Minecraft's own textures and remain Mojang's property. No texture
from any stone mod ships in this jar; each stone is referenced by its id.

Built on [MultiLoader Template](https://github.com/jaredlll08/MultiLoader-Template) by jaredlll08.
