package com.chillpavz.seamlessoresmatrix.content;

import com.chillpavz.seamlessoresmatrix.platform.Services;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.material.MapColor;

import java.util.Collections;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;

/**
 * A modded stone that ore ends up inside, because the stone is placed after the ore.
 *
 * <p>Declared by id, never by Block reference: the stone belongs to another mod, which may register
 * after us, and this mod never compiles against it. The block itself is looked up when it is first
 * needed, which is always after every mod has registered.
 *
 * <p>{@code ores} is the measured pair list, not a taste call: every ore that reaches this stone's
 * height band in its biome at a rate above the floor. A missing pair is a visible bug, because the
 * stone swallows that ore regardless.
 */
public final class HostStone {

    /** Which vanilla ore strength a variant takes: the stone ore's or the deepslate ore's. */
    public enum Strength { STONE, DEEPSLATE }

    // Blockus: Fabric only. Map colours read from BlockusBlocks. Limestone, marble and bluestone copy
    // stone's properties and viridite copies deepslate's, which is what the ore strength follows.
    public static final HostStone BLOCKUS_LIMESTONE = new HostStone("blockus", "limestone",
            Strength.STONE, MapColor.WOOD, EnumSet.allOf(OreKind.class));
    public static final HostStone BLOCKUS_MARBLE = new HostStone("blockus", "marble",
            Strength.STONE, MapColor.QUARTZ, EnumSet.allOf(OreKind.class));
    public static final HostStone BLOCKUS_BLUESTONE = new HostStone("blockus", "bluestone",
            Strength.STONE, MapColor.COLOR_CYAN, EnumSet.allOf(OreKind.class));
    // Deep and deep dark only: no coal, no emerald, and copper falls just under the floor.
    public static final HostStone BLOCKUS_VIRIDITE = new HostStone("blockus", "viridite",
            Strength.DEEPSLATE, MapColor.PLANT,
            EnumSet.of(OreKind.IRON, OreKind.GOLD, OreKind.REDSTONE, OreKind.LAPIS, OreKind.DIAMOND));
    // Wilder Wild: both loaders. Only in its magmatic caves biome, which lists no emerald. Map colour
    // and hardness (4.5, so the deepslate ore strength) read from the running game.
    public static final HostStone WILDERWILD_GABBRO = new HostStone("wilderwild", "gabbro",
            Strength.DEEPSLATE, MapColor.TERRACOTTA_BROWN, EnumSet.complementOf(EnumSet.of(OreKind.EMERALD)));

    public static final List<HostStone> ALL = List.of(
            BLOCKUS_LIMESTONE, BLOCKUS_MARBLE, BLOCKUS_BLUESTONE, BLOCKUS_VIRIDITE, WILDERWILD_GABBRO);

    private final String modId;
    private final String path;
    private final Strength strength;
    private final MapColor mapColor;
    private final Set<OreKind> ores;
    private volatile Block block;

    private HostStone(String modId, String path, Strength strength, MapColor mapColor, Set<OreKind> ores) {
        this.modId = modId;
        this.path = path;
        this.strength = strength;
        this.mapColor = mapColor;
        // An EnumSet, not Set.copyOf: that one's iteration order changes from run to run, and this
        // order is the registration and creative tab order.
        this.ores = Collections.unmodifiableSet(EnumSet.copyOf(ores));
    }

    public String modId() {
        return modId;
    }

    public Identifier id() {
        return Identifier.fromNamespaceAndPath(modId, path);
    }

    /** Id prefix for our variants. Carries the mod, because Create and Blockus both have a limestone. */
    public String name() {
        return modId + "_" + path;
    }

    public Strength strength() {
        return strength;
    }

    public MapColor mapColor() {
        return mapColor;
    }

    public Set<OreKind> ores() {
        return ores;
    }

    public boolean isLoaded() {
        return Services.PLATFORM.isModLoaded(modId);
    }

    /**
     * The stone itself, or null if its mod is absent or the id does not resolve. Only call once every
     * mod has registered, i.e. never during our own registration.
     */
    public Block block() {
        Block found = block;
        if (found == null) {
            found = BuiltInRegistries.BLOCK.getOptional(id()).orElse(null);
            block = found;
        }
        return found;
    }

    @Override
    public String toString() {
        return id().toString();
    }
}
