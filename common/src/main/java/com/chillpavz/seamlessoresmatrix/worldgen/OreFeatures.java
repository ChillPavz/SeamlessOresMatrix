package com.chillpavz.seamlessoresmatrix.worldgen;

import com.chillpavz.seamlessoresmatrix.Constants;
import net.minecraft.core.Holder;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.levelgen.feature.AbstractOreFeature;
import net.minecraft.world.level.levelgen.feature.BlockReplacement;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.OreFeature;
import net.minecraft.world.level.levelgen.feature.ScatteredOreFeature;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/** What both injectors share: which features they may rebuild, and how. */
final class OreFeatures {

    private OreFeatures() {}

    /** Mod subclasses already reported, so each is logged once per session rather than per world. */
    private static final Set<String> REPORTED = ConcurrentHashMap.newKeySet();

    /**
     * True for exactly vanilla's two ore classes. A mod's own AbstractOreFeature subclass may carry
     * state or a constructor contract we cannot reproduce, so it is left alone, and said so once.
     */
    static boolean rebuildable(Feature feature, String injector) {
        final Class<?> kind = feature.getClass();
        if (kind == OreFeature.class || kind == ScatteredOreFeature.class) {
            return true;
        }
        if (REPORTED.add(injector + " " + kind.getName())) {
            Constants.LOG.info("{}: left {} alone, it is not a vanilla ore feature", injector, kind.getName());
        }
        return false;
    }

    static boolean placesAny(List<BlockReplacement> targets, Map<Block, ?> blocks) {
        for (BlockReplacement target : targets) {
            if (blocks.containsKey(target.state().getBlock())) {
                return true;
            }
        }
        return false;
    }

    /**
     * Rebinds the holder to the same kind of feature with {@code extra} in FRONT of its own targets.
     * First match wins, so anything appended would never be reached.
     *
     * <p>Rebinding a {@code Holder<Feature>} is safe after the feature-order table exists: the
     * PlacedFeature that owns this holder is untouched, so the table's key still matches. Rebinding a
     * PlacedFeature would not be. Never do that from here.
     */
    @SuppressWarnings({"unchecked", "rawtypes"})
    static void prepend(Holder.Reference<Feature> holder, AbstractOreFeature ore, List<BlockReplacement> extra) {
        final List<BlockReplacement> merged = new ArrayList<>(extra);
        merged.addAll(ore.targetStates());
        final Feature rebuilt = ore.getClass() == ScatteredOreFeature.class
                ? new ScatteredOreFeature(List.copyOf(merged), ore.size(), ore.discardChanceOnAirExposure())
                : new OreFeature(List.copyOf(merged), ore.size(), ore.discardChanceOnAirExposure());
        // bindValue is protected in vanilla; opened by the access widener / access transformer.
        ((Holder.Reference) holder).bindValue(rebuilt);
    }
}
