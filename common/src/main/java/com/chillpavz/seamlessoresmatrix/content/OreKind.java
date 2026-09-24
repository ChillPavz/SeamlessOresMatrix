package com.chillpavz.seamlessoresmatrix.content;

import com.chillpavz.seamlessoresmatrix.platform.Services;
import net.minecraft.resources.Identifier;
import net.minecraft.util.valueproviders.ConstantInt;
import net.minecraft.util.valueproviders.IntProvider;
import net.minecraft.util.valueproviders.UniformInt;

import java.util.List;

/**
 * An ore that a host stone can swallow: the eight overworld ores, Create's zinc, and the two nether
 * ores that Create's nether strata reach.
 *
 * <p>Each kind stands for EVERY one of its forms: a limestone blob placed over deepslate iron leaves a
 * deepslate iron ore inside limestone just as surely as it does a stone one, and both become the same
 * limestone iron ore. The nether ores have one form only.
 *
 * <p>XP matches the ore's own, which vanilla keeps the same for a stone ore and its deepslate form.
 */
public enum OreKind {
    COAL("coal", UniformInt.of(0, 2)),
    IRON("iron", ConstantInt.of(0)),
    COPPER("copper", ConstantInt.of(0)),
    GOLD("gold", ConstantInt.of(0)),
    REDSTONE("redstone", ConstantInt.of(0)),
    EMERALD("emerald", UniformInt.of(3, 7)),
    LAPIS("lapis", UniformInt.of(2, 5)),
    DIAMOND("diamond", UniformInt.of(3, 7)),
    // Create's zinc: a variant exists only while Create is installed. Create builds its zinc ores from
    // gold ore's properties, so ours do too; the drops are Create's own.
    ZINC("zinc", ConstantInt.of(0), "create",
            Identifier.fromNamespaceAndPath("create", "zinc_ore"),
            Identifier.fromNamespaceAndPath("create", "deepslate_zinc_ore"),
            Identifier.withDefaultNamespace("gold_ore"), Identifier.withDefaultNamespace("deepslate_gold_ore"),
            List.of("granite", "diorite", "andesite", "tuff")),
    NETHER_GOLD("nether_gold", UniformInt.of(0, 1), null,
            Identifier.withDefaultNamespace("nether_gold_ore"), null,
            Identifier.withDefaultNamespace("nether_gold_ore"), null,
            List.of("basalt", "blackstone")),
    QUARTZ("quartz", UniformInt.of(2, 5), null,
            Identifier.withDefaultNamespace("nether_quartz_ore"), null,
            Identifier.withDefaultNamespace("nether_quartz_ore"), null,
            List.of("basalt", "blackstone"));

    private final String id;
    private final IntProvider xp;
    private final String modId;
    private final Identifier stoneOre;
    private final Identifier deepslateOre;
    private final Identifier stoneStrength;
    private final Identifier deepslateStrength;
    private final List<String> seamlessOresHosts;

    /** A vanilla overworld ore: minecraft:X_ore and minecraft:deepslate_X_ore. */
    OreKind(String id, IntProvider xp) {
        this(id, xp, null, Identifier.withDefaultNamespace(id + "_ore"),
                Identifier.withDefaultNamespace("deepslate_" + id + "_ore"),
                Identifier.withDefaultNamespace(id + "_ore"),
                Identifier.withDefaultNamespace("deepslate_" + id + "_ore"),
                // Seamless Ores' hosts of an overworld ore. Written out here: an enum constructor cannot
                // read a static field of its own enum, which is still unset while the constants are built.
                List.of("granite", "diorite", "andesite", "tuff"));
    }

    OreKind(String id, IntProvider xp, String modId, Identifier stoneOre, Identifier deepslateOre,
            Identifier stoneStrength, Identifier deepslateStrength, List<String> seamlessOresHosts) {
        this.id = id;
        this.xp = xp;
        this.modId = modId;
        this.stoneOre = stoneOre;
        this.deepslateOre = deepslateOre;
        this.stoneStrength = stoneStrength;
        this.deepslateStrength = deepslateStrength;
        this.seamlessOresHosts = seamlessOresHosts;
    }

    /** Id fragment, e.g. {@code iron} in {@code blockus_limestone_iron_ore}. */
    public String id() {
        return id;
    }

    public IntProvider xp() {
        return xp;
    }

    /** Whether this ore exists in this game: always for vanilla's, only with its mod for a modded one. */
    public boolean isLoaded() {
        return modId == null || Services.PLATFORM.isModLoaded(modId);
    }

    /** Every block that IS this ore before a stone swallows it: the stone form, then the deepslate one. */
    public List<Identifier> forms() {
        return deepslateOre == null ? List.of(stoneOre) : List.of(stoneOre, deepslateOre);
    }

    /** Seamless Ores' own variants of this ore, which a modded stone swallows just the same. */
    public List<Identifier> seamlessOresForms() {
        return seamlessOresHosts.stream()
                .map(host -> Identifier.fromNamespaceAndPath("seamlessores", host + "_" + seamlessOresId() + "_ore"))
                .toList();
    }

    /** Seamless Ores names its nether gold after the metal alone: {@code basalt_gold_ore}. */
    private String seamlessOresId() {
        return this == NETHER_GOLD ? "gold" : id;
    }

    /**
     * The block whose hardness, blast resistance and tool requirement a variant copies. Vanilla, so it is
     * registered before we are; the nether ores have one strength whatever the host.
     */
    public Identifier strengthSource(HostStone.Strength strength) {
        return strength == HostStone.Strength.DEEPSLATE && deepslateStrength != null ? deepslateStrength : stoneStrength;
    }

    /** Redstone ore is a RedStoneOreBlock (lit state, random ticks), not a DropExperienceBlock. */
    public boolean redstoneLike() {
        return this == REDSTONE;
    }
}
