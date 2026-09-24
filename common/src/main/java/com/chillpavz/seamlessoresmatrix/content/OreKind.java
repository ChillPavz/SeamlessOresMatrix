package com.chillpavz.seamlessoresmatrix.content;

import net.minecraft.resources.Identifier;
import net.minecraft.util.valueproviders.ConstantInt;
import net.minecraft.util.valueproviders.IntProvider;
import net.minecraft.util.valueproviders.UniformInt;

/**
 * An ore that a host stone can swallow. Only the eight overworld ores for now; modded ores join in
 * later waves.
 *
 * <p>Each kind stands for BOTH of its vanilla forms: a limestone blob placed over deepslate iron
 * leaves a deepslate iron ore inside limestone just as surely as it does a stone one, and both become
 * the same limestone iron ore.
 *
 * <p>XP matches vanilla, which uses the same value for a stone ore and its deepslate form.
 */
public enum OreKind {
    COAL("coal", UniformInt.of(0, 2)),
    IRON("iron", ConstantInt.of(0)),
    COPPER("copper", ConstantInt.of(0)),
    GOLD("gold", ConstantInt.of(0)),
    REDSTONE("redstone", ConstantInt.of(0)),
    EMERALD("emerald", UniformInt.of(3, 7)),
    LAPIS("lapis", UniformInt.of(2, 5)),
    DIAMOND("diamond", UniformInt.of(3, 7));

    private final String id;
    private final IntProvider xp;

    OreKind(String id, IntProvider xp) {
        this.id = id;
        this.xp = xp;
    }

    /** Id fragment, e.g. {@code iron} in {@code blockus_limestone_iron_ore}. */
    public String id() {
        return id;
    }

    public IntProvider xp() {
        return xp;
    }

    public Identifier stoneOre() {
        return Identifier.withDefaultNamespace(id + "_ore");
    }

    public Identifier deepslateOre() {
        return Identifier.withDefaultNamespace("deepslate_" + id + "_ore");
    }

    /** Redstone ore is a RedStoneOreBlock (lit state, random ticks), not a DropExperienceBlock. */
    public boolean redstoneLike() {
        return this == REDSTONE;
    }
}
