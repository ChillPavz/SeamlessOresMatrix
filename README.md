# Seamless Ores: Matrix

Ore blocks that match the modded stone they generate in. When a stone from another mod forms around
ore, the ore normally keeps its plain stone or deepslate look and shows up as a square of the wrong
rock. Matrix gives that ore the stone it actually sits in.

**It adds no ore.** The same veins, in the same places and the same amounts, drawn to fit their
surroundings.

| | |
|---|---|
| Minecraft | 26.1.x, 26.2, 26.3 (one jar for all of them) |
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
  the other mod's own ore, read from that mod.
- Every overlay is hand drawn and shared with Seamless Ores. The stone itself is drawn by the mod
  that adds it, so a resource pack that retextures that stone restyles these ores too.
- A variant only exists when its stone's mod is installed, and for another mod's ore that mod as
  well. With no supported stone mod, Matrix does nothing at all.
- Ores from Create, Energized Power, Mystical Agriculture, Mythic Metals, Mythic Upgrades,
  Occultism, Powah, Silent Gear, Silent's Gems and Tech Reborn are covered wherever they meet a
  supported stone.

## Companion resource pack

[Seamless Glowing Ores](https://modrinth.com/resourcepack/seamless-glowing-ores) makes every ore
glow, with an optional connected outline that joins touching ore of the same type across different
host stones. It covers Matrix's blocks as well as Seamless Ores'.

## Block list

<!-- BEGIN GENERATED block-list -->
**714 blocks** in the `seamlessoresmatrix` namespace. Each exists only when the mod that places its stone is installed, and one of another mod's ore only with that mod as well. A block's id is `<stone>_<ore>_ore`, from the two columns below: `blockus_limestone` and `iron` make `blockus_limestone_iron_ore`.

**Blockus, requires `blockus`** (Fabric, 26.1.x to 26.3)

Stones: Limestone `blockus_limestone`, Marble `blockus_marble`, Bluestone `blockus_bluestone`, Viridite `blockus_viridite`

| Ore | `<ore>` | Also requires | In |
|---|---|---|---|
| Coal | `coal` |  | Limestone, Marble, Bluestone |
| Iron | `iron` |  | every stone |
| Copper | `copper` |  | Limestone, Marble, Bluestone |
| Gold | `gold` |  | every stone |
| Redstone | `redstone` |  | every stone |
| Emerald | `emerald` |  | Limestone, Marble, Bluestone |
| Lapis Lazuli | `lapis` |  | every stone |
| Diamond | `diamond` |  | every stone |
| Zinc | `zinc` | Create `create` | every stone |
| Energized Tin | `energized_tin` | Energized Power `energizedpower` | Limestone, Marble |
| Adamantite | `adamantite` | Mythic Metals `mythicmetals` | Bluestone, Viridite |
| Aquarium | `aquarium` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Banglum | `banglum` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Carmot | `carmot` | Mythic Metals `mythicmetals` | every stone |
| Kyber | `kyber` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Manganese | `manganese` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Morkite | `morkite` | Mythic Metals `mythicmetals` | every stone |
| Mythril | `mythril` | Mythic Metals `mythicmetals` | every stone |
| Orichalcum | `orichalcum` | Mythic Metals `mythicmetals` | every stone |
| Osmium | `osmium` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Platinum | `platinum` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Prometheum | `prometheum` | Mythic Metals `mythicmetals` | every stone |
| Quadrillum | `quadrillum` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Runite | `runite` | Mythic Metals `mythicmetals` | every stone |
| Silver | `silver` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Starrite | `starrite` | Mythic Metals `mythicmetals` | Limestone |
| Tin | `tin` | Mythic Metals `mythicmetals` | Limestone, Marble |
| Unobtainium | `unobtainium` | Mythic Metals `mythicmetals` | every stone |
| Aquamarine | `aquamarine` | Mythic Upgrades `mythicupgrades` | every stone |
| Citrine | `citrine` | Mythic Upgrades `mythicupgrades` | every stone |
| Necoium | `necoium` | Mythic Upgrades `mythicupgrades` | every stone |
| Peridot | `peridot` | Mythic Upgrades `mythicupgrades` | every stone |
| Topaz | `topaz` | Mythic Upgrades `mythicupgrades` | every stone |
| Tech Reborn Bauxite | `techreborn_bauxite` | Tech Reborn `techreborn` | every stone |
| Galena | `galena` | Tech Reborn `techreborn` | every stone |
| Iridium | `iridium` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Lead | `techreborn_lead` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Ruby | `techreborn_ruby` | Tech Reborn `techreborn` | Limestone, Marble |
| Tech Reborn Sapphire | `techreborn_sapphire` | Tech Reborn `techreborn` | Limestone, Marble |
| Tech Reborn Silver | `techreborn_silver` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Tin | `techreborn_tin` | Tech Reborn `techreborn` | Limestone, Marble |
| Tech Reborn Uranium | `techreborn_uranium` | Tech Reborn `techreborn` | every stone |

**Create, requires `create`** (Create Fly, Fabric, 26.1.2 and 26.2)

Stones: Asurine `create_asurine`, Crimsite `create_crimsite`, Limestone `create_limestone`, Ochrum `create_ochrum`, Scorchia `create_scorchia`, Scoria `create_scoria`, Veridium `create_veridium`, Calcite `minecraft_calcite`, Dripstone `minecraft_dripstone_block`, Smooth Basalt `minecraft_smooth_basalt`

| Ore | `<ore>` | Also requires | In |
|---|---|---|---|
| Coal | `coal` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Iron | `iron` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Copper | `copper` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Gold | `gold` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Redstone | `redstone` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Emerald | `emerald` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Lapis Lazuli | `lapis` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Diamond | `diamond` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Zinc | `zinc` |  | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Nether Gold | `nether_gold` |  | Scorchia, Scoria, Smooth Basalt |
| Nether Quartz | `quartz` |  | Scorchia, Scoria, Smooth Basalt |
| Energized Tin | `energized_tin` | Energized Power `energizedpower` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Adamantite | `adamantite` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Aquarium | `aquarium` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Banglum | `banglum` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Carmot | `carmot` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Kyber | `kyber` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Manganese | `manganese` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Midas Gold | `midas_gold` | Mythic Metals `mythicmetals` | Scorchia, Scoria, Smooth Basalt |
| Morkite | `morkite` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Mythril | `mythril` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Nether Banglum | `nether_banglum` | Mythic Metals `mythicmetals` | Scorchia, Scoria, Smooth Basalt |
| Orichalcum | `orichalcum` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Osmium | `osmium` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Palladium | `palladium` | Mythic Metals `mythicmetals` | Scorchia, Scoria, Smooth Basalt |
| Platinum | `platinum` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Prometheum | `prometheum` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Quadrillum | `quadrillum` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Runite | `runite` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Silver | `silver` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Stormyx | `stormyx` | Mythic Metals `mythicmetals` | Scorchia, Scoria, Smooth Basalt |
| Tin | `tin` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Unobtainium | `unobtainium` | Mythic Metals `mythicmetals` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Aquamarine | `aquamarine` | Mythic Upgrades `mythicupgrades` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Citrine | `citrine` | Mythic Upgrades `mythicupgrades` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Necoium | `necoium` | Mythic Upgrades `mythicupgrades` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Peridot | `peridot` | Mythic Upgrades `mythicupgrades` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Ruby | `ruby` | Mythic Upgrades `mythicupgrades` | Scorchia, Scoria, Smooth Basalt |
| Sapphire | `sapphire` | Mythic Upgrades `mythicupgrades` | Scorchia, Scoria, Smooth Basalt |
| Topaz | `topaz` | Mythic Upgrades `mythicupgrades` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Tech Reborn Bauxite | `techreborn_bauxite` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Cinnabar | `cinnabar` | Tech Reborn `techreborn` | Scorchia, Scoria, Smooth Basalt |
| Galena | `galena` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Iridium | `iridium` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Tech Reborn Lead | `techreborn_lead` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Pyrite | `pyrite` | Tech Reborn `techreborn` | Scorchia, Scoria, Smooth Basalt |
| Tech Reborn Ruby | `techreborn_ruby` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Tech Reborn Sapphire | `techreborn_sapphire` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Tech Reborn Silver | `techreborn_silver` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Sphalerite | `sphalerite` | Tech Reborn `techreborn` | Scorchia, Scoria, Smooth Basalt |
| Tech Reborn Tin | `techreborn_tin` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |
| Tech Reborn Uranium | `techreborn_uranium` | Tech Reborn `techreborn` | Asurine, Crimsite, Limestone, Ochrum, Scoria, Veridium, Calcite, Dripstone, Smooth Basalt |

**Forbidden and Arcanus, requires `forbidden_arcanus`** (NeoForge, 26.1.2)

Stones: Darkstone `forbidden_arcanus_darkstone`

| Ore | `<ore>` | Also requires | In |
|---|---|---|---|
| Iron | `iron` |  | Darkstone |
| Gold | `gold` |  | Darkstone |
| Redstone | `redstone` |  | Darkstone |
| Lapis Lazuli | `lapis` |  | Darkstone |
| Diamond | `diamond` |  | Darkstone |
| Prosperity | `prosperity` | Mystical Agriculture `mysticalagriculture` | Darkstone |
| Occultism Silver | `occultism_silver` | Occultism `occultism` | Darkstone |
| Uraninite | `uraninite` | Powah `powah` | Darkstone |
| Uraninite Dense | `uraninite_dense` | Powah `powah` | Darkstone |
| Uraninite Poor | `uraninite_poor` | Powah `powah` | Darkstone |
| Bort | `bort` | Silent Gear `silentgear` | Darkstone |
| Alexandrite | `alexandrite` | Silent's Gems `silentgems` | Darkstone |
| Silent's Aquamarine | `silents_aquamarine` | Silent's Gems `silentgems` | Darkstone |
| Chaos | `chaos` | Silent's Gems `silentgems` | Darkstone |
| Garnet | `garnet` | Silent's Gems `silentgems` | Darkstone |
| Heliodor | `heliodor` | Silent's Gems `silentgems` | Darkstone |
| Iolite | `iolite` | Silent's Gems `silentgems` | Darkstone |
| Opal | `opal` | Silent's Gems `silentgems` | Darkstone |
| Silent's Peridot | `silents_peridot` | Silent's Gems `silentgems` | Darkstone |
| Silent's Ruby | `silents_ruby` | Silent's Gems `silentgems` | Darkstone |
| Silent's Sapphire | `silents_sapphire` | Silent's Gems `silentgems` | Darkstone |
| Silent's Silver | `silents_silver` | Silent's Gems `silentgems` | Darkstone |
| Silent's Topaz | `silents_topaz` | Silent's Gems `silentgems` | Darkstone |
| Turquoise | `turquoise` | Silent's Gems `silentgems` | Darkstone |

**Mythic Upgrades, requires `mythicupgrades`** (Fabric and NeoForge, 26.2 and 26.3)

Stones: Aquamarine Schist `mythicupgrades_aquamarine_schist`, Citrine Schist `mythicupgrades_citrine_schist`, Peridot Schist `mythicupgrades_peridot_schist`, Topaz Schist `mythicupgrades_topaz_schist`, Sapphire Schist `mythicupgrades_sapphire_schist`

| Ore | `<ore>` | Also requires | In |
|---|---|---|---|
| Coal | `coal` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Iron | `iron` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Copper | `copper` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Gold | `gold` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Redstone | `redstone` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Lapis Lazuli | `lapis` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Diamond | `diamond` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Aquamarine | `aquamarine` |  | Peridot Schist |
| Citrine | `citrine` |  | Topaz Schist |
| Necoium | `necoium` |  | Aquamarine Schist, Citrine Schist, Peridot Schist, Topaz Schist |
| Ruby | `ruby` |  | Sapphire Schist |

**Promenade, requires `promenade`** (Fabric, 26.1.x and 26.2)

Stones: Asphalt `promenade_asphalt`, Blunite `promenade_blunite`

| Ore | `<ore>` | Also requires | In |
|---|---|---|---|
| Coal | `coal` |  | every stone |
| Iron | `iron` |  | every stone |
| Copper | `copper` |  | every stone |
| Gold | `gold` |  | every stone |
| Redstone | `redstone` |  | every stone |
| Emerald | `emerald` |  | every stone |
| Lapis Lazuli | `lapis` |  | every stone |
| Diamond | `diamond` |  | every stone |
| Zinc | `zinc` | Create `create` | every stone |
| Energized Tin | `energized_tin` | Energized Power `energizedpower` | every stone |
| Aquarium | `aquarium` | Mythic Metals `mythicmetals` | every stone |
| Banglum | `banglum` | Mythic Metals `mythicmetals` | every stone |
| Carmot | `carmot` | Mythic Metals `mythicmetals` | every stone |
| Kyber | `kyber` | Mythic Metals `mythicmetals` | every stone |
| Manganese | `manganese` | Mythic Metals `mythicmetals` | every stone |
| Morkite | `morkite` | Mythic Metals `mythicmetals` | every stone |
| Mythril | `mythril` | Mythic Metals `mythicmetals` | every stone |
| Orichalcum | `orichalcum` | Mythic Metals `mythicmetals` | every stone |
| Osmium | `osmium` | Mythic Metals `mythicmetals` | every stone |
| Platinum | `platinum` | Mythic Metals `mythicmetals` | every stone |
| Prometheum | `prometheum` | Mythic Metals `mythicmetals` | every stone |
| Quadrillum | `quadrillum` | Mythic Metals `mythicmetals` | every stone |
| Runite | `runite` | Mythic Metals `mythicmetals` | every stone |
| Silver | `silver` | Mythic Metals `mythicmetals` | every stone |
| Starrite | `starrite` | Mythic Metals `mythicmetals` | every stone |
| Tin | `tin` | Mythic Metals `mythicmetals` | every stone |
| Unobtainium | `unobtainium` | Mythic Metals `mythicmetals` | every stone |
| Aquamarine | `aquamarine` | Mythic Upgrades `mythicupgrades` | every stone |
| Citrine | `citrine` | Mythic Upgrades `mythicupgrades` | every stone |
| Necoium | `necoium` | Mythic Upgrades `mythicupgrades` | every stone |
| Peridot | `peridot` | Mythic Upgrades `mythicupgrades` | every stone |
| Topaz | `topaz` | Mythic Upgrades `mythicupgrades` | every stone |
| Tech Reborn Bauxite | `techreborn_bauxite` | Tech Reborn `techreborn` | every stone |
| Galena | `galena` | Tech Reborn `techreborn` | every stone |
| Iridium | `iridium` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Lead | `techreborn_lead` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Ruby | `techreborn_ruby` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Sapphire | `techreborn_sapphire` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Silver | `techreborn_silver` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Tin | `techreborn_tin` | Tech Reborn `techreborn` | every stone |
| Tech Reborn Uranium | `techreborn_uranium` | Tech Reborn `techreborn` | every stone |

**Wilder Wild, requires `wilderwild`** (Fabric 26.1.x to 26.3, NeoForge 26.2 and 26.3)

Stones: Gabbro `wilderwild_gabbro`

| Ore | `<ore>` | Also requires | In |
|---|---|---|---|
| Coal | `coal` |  | Gabbro |
| Iron | `iron` |  | Gabbro |
| Copper | `copper` |  | Gabbro |
| Gold | `gold` |  | Gabbro |
| Redstone | `redstone` |  | Gabbro |
| Lapis Lazuli | `lapis` |  | Gabbro |
| Diamond | `diamond` |  | Gabbro |
| Zinc | `zinc` | Create `create` | Gabbro |
| Energized Tin | `energized_tin` | Energized Power `energizedpower` | Gabbro |
| Adamantite | `adamantite` | Mythic Metals `mythicmetals` | Gabbro |
| Aquarium | `aquarium` | Mythic Metals `mythicmetals` | Gabbro |
| Banglum | `banglum` | Mythic Metals `mythicmetals` | Gabbro |
| Carmot | `carmot` | Mythic Metals `mythicmetals` | Gabbro |
| Kyber | `kyber` | Mythic Metals `mythicmetals` | Gabbro |
| Manganese | `manganese` | Mythic Metals `mythicmetals` | Gabbro |
| Morkite | `morkite` | Mythic Metals `mythicmetals` | Gabbro |
| Mythril | `mythril` | Mythic Metals `mythicmetals` | Gabbro |
| Orichalcum | `orichalcum` | Mythic Metals `mythicmetals` | Gabbro |
| Osmium | `osmium` | Mythic Metals `mythicmetals` | Gabbro |
| Platinum | `platinum` | Mythic Metals `mythicmetals` | Gabbro |
| Prometheum | `prometheum` | Mythic Metals `mythicmetals` | Gabbro |
| Quadrillum | `quadrillum` | Mythic Metals `mythicmetals` | Gabbro |
| Runite | `runite` | Mythic Metals `mythicmetals` | Gabbro |
| Silver | `silver` | Mythic Metals `mythicmetals` | Gabbro |
| Tin | `tin` | Mythic Metals `mythicmetals` | Gabbro |
| Unobtainium | `unobtainium` | Mythic Metals `mythicmetals` | Gabbro |
| Necoium | `necoium` | Mythic Upgrades `mythicupgrades` | Gabbro |
| Occultism Silver | `occultism_silver` | Occultism `occultism` | Gabbro |
| Tech Reborn Bauxite | `techreborn_bauxite` | Tech Reborn `techreborn` | Gabbro |
| Galena | `galena` | Tech Reborn `techreborn` | Gabbro |
| Iridium | `iridium` | Tech Reborn `techreborn` | Gabbro |
| Tech Reborn Lead | `techreborn_lead` | Tech Reborn `techreborn` | Gabbro |
| Tech Reborn Ruby | `techreborn_ruby` | Tech Reborn `techreborn` | Gabbro |
| Tech Reborn Sapphire | `techreborn_sapphire` | Tech Reborn `techreborn` | Gabbro |
| Tech Reborn Silver | `techreborn_silver` | Tech Reborn `techreborn` | Gabbro |
| Tech Reborn Tin | `techreborn_tin` | Tech Reborn `techreborn` | Gabbro |
| Tech Reborn Uranium | `techreborn_uranium` | Tech Reborn `techreborn` | Gabbro |
<!-- END GENERATED block-list -->

## Configuration

One switch per stone, grouped by the mod that places it; a group is hidden when its mod is not
installed. Every switch gates **worldgen only, never registration**, so a client and a server cannot
disagree about which blocks exist. Turning a stone off means its ore keeps the vanilla look in newly
generated chunks. The blocks still exist, and chunks that already generated never change.

Settings take effect the next time a world is loaded.

## For resource pack authors

<!-- BEGIN GENERATED overlay-list -->
Every variant of one ore shares a single overlay texture, so covering all 714 blocks takes **73 PNG files**:

```
assets/seamlessoresmatrix/textures/block/<ore>_overlay.png
```

where `<ore>` is one of: `adamantite` `alexandrite` `aquamarine` `aquarium` `banglum` `bort` `carmot` `chaos` `cinnabar` `citrine` `coal` `copper` `diamond` `emerald` `energized_tin` `galena` `garnet` `gold` `heliodor` `iolite` `iridium` `iron` `kyber` `lapis` `manganese` `midas_gold` `morkite` `mythril` `necoium` `nether_banglum` `nether_gold` `occultism_silver` `opal_darkstone` `orichalcum` `osmium` `palladium` `peridot` `platinum` `prometheum` `prosperity` `pyrite` `quadrillum` `quartz` `redstone` `ruby` `runite` `sapphire` `silents_aquamarine` `silents_peridot` `silents_ruby` `silents_sapphire` `silents_silver` `silents_topaz` `silver` `sphalerite` `starrite` `stormyx` `techreborn_bauxite` `techreborn_lead` `techreborn_ruby` `techreborn_sapphire` `techreborn_silver` `techreborn_tin` `techreborn_uranium` `tin` `topaz` `turquoise` `unobtainium` `unobtainium_deepslate` `uraninite` `uraninite_dense` `uraninite_poor` `zinc`

Two keys are not an ore id. `unobtainium_deepslate` is Mythic Metals' deepslate look, worn in the stones as hard as deepslate. `opal_darkstone` is opal painted onto darkstone: opal is translucent, so each rock takes its own precomposited overlay.
<!-- END GENERATED overlay-list -->

Each file is the ore layer only, blobs on transparency. The host stone is referenced straight from
its own mod, so you do not supply it.

## Building

Requires JDK 25 and Python 3. One source tree builds every Minecraft version, and one jar per loader
runs on all of them:

```
./gradlew build -Pmc=26.3
./gradlew build -Pmc=26.1.x
python tools/merge_bands.py
```

The merge leaves `seamlessoresmatrix-<loader>-26.x-<version>.jar` in `fabric/build/libs` and
`neoforge/build/libs`. It is the 26.1.x build, compiled against 26.1.2, plus the one worldgen class
that has to be compiled against 26.3; the mod picks the matching one when the game starts. The merge
stops if the two builds differ anywhere else. `-Pmc=26.2` builds a jar for 26.2 alone, which is only a
compile check. `26.3` is the default band.

Blockstates, models, lang, loot tables, tags and this README's block list are generated from the
host table in `common/.../content/HostStone.java` and the measured pairs in `tools/modded_pairs.json`:

```
python tools/generate_assets.py
```

It reads loot tables from the 26.3 and 26.1.2 Minecraft client jars (which a build of each version
leaves in the Gradle cache), and each other mod's loot, tool tiers and ore tags from that mod's own
jar, listed in `MOD_JARS` at the top of the script.

## Project layout

| Path | What it holds |
|---|---|
| `versions/` | One properties file per Minecraft version: Minecraft, loader, Cloth and Mod Menu versions |
| `common/src/main` | Everything shared: the host table, content registration, both worldgen injectors, config holder |
| `common/src/era263`, `common/src/era261` | What changed shape at 26.3: how ore features are read and rebuilt (`Era263`, `Era261`), and the access widener and transformer. `era261` serves 26.1.x and 26.2 |
| `common/src/main/resources/era26*`, `mc26.*` | Loot tables per Minecraft version, as pack overlays that `pack.mcmeta` turns on by data format |
| `fabric/`, `neoforge/` | Loader entry points, the Cloth Config data class and screen |
| `tools/generate_assets.py` | Generates assets, data and the block list above |
| `tools/merge_bands.py` | Joins the 26.1.x and 26.3 builds into one jar per loader |

The Cloth Config classes are duplicated across both loader modules on purpose and must stay
identical. Their switches are generated from the host table. They cannot live in `common`, because loader dependencies are not on its classpath.

## Credits

<!-- BEGIN GENERATED credits -->
The vanilla ore overlays are derived from Minecraft's own textures and remain Mojang's
property. Each other mod's overlay is derived from that mod's own ore texture, so it is
theirs and is used under the licence shown:

| Mod | Author | Licence |
|---|---|---|
| Create | - | MIT |
| Energized Power | JDDev0 | MIT |
| Mystical Agriculture | BlakeBr0 | MIT |
| Mythic Metals | Noaaan | MIT |
| Mythic Upgrades | TriQue | MIT |
| Occultism | Kli Kli | MIT |
| Powah | owmii, Technici4n, shartte | LGPL-3.0 |
| Silent Gear | SilentChaos512 | MIT |
| Silent's Gems | SilentChaos512 | MIT |
| Tech Reborn | Team Reborn, modmuss50, drcrazy | MIT |

No texture from any stone mod ships in this jar; each stone is referenced by its id.
<!-- END GENERATED credits -->

Built on [MultiLoader Template](https://github.com/jaredlll08/MultiLoader-Template) by jaredlll08.
