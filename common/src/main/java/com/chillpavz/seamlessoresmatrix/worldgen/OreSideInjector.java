package com.chillpavz.seamlessoresmatrix.worldgen;

import com.chillpavz.seamlessoresmatrix.Constants;
import com.chillpavz.seamlessoresmatrix.MatrixConfig;
import com.chillpavz.seamlessoresmatrix.content.MatrixContent;
import com.chillpavz.seamlessoresmatrix.content.Variant;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.levelgen.feature.AbstractOreFeature;
import net.minecraft.world.level.levelgen.feature.BlockReplacement;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.structure.templatesystem.BlockMatchTest;
import net.minecraft.world.level.levelgen.structure.templatesystem.RuleTest;

import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;

/**
 * Restyles ore placed INTO a modded stone that was already there, by extending the ORE's feature.
 *
 * <p>The mirror of {@link StoneSideInjector}. Several of the stones are in the ore replaceables tags
 * (Blockus limestone and marble in the stone one, bluestone, viridite and gabbro in the deepslate one),
 * so any ore feature that runs AFTER such a stone places its plain ore inside it. Whether that happens
 * depends on load order, so both sides are covered and the result does not.
 *
 * <p>Each added replacement is {@code all_of(original target, block_match <stone>) -> variant}, put in
 * front of the original. It can only fire where the feature would have placed that very ore, so it
 * inherits every height rule the original has, including 26.3's height-specific tuff split.
 */
public final class OreSideInjector {

    static final String NAME = "Ore side";

    private OreSideInjector() {}

    public static void inject(RegistryAccess registries) {

        final Map<Block, Variant> ours = MatrixContent.byBlock();
        // Which of our blocks stand in for each vanilla ore block, stone and deepslate form alike.
        final Map<Block, List<Map.Entry<Block, Block>>> byOre = new IdentityHashMap<>();
        ours.forEach((block, variant) -> {
            final Block stone = variant.host().block();
            if (stone == null || !MatrixConfig.isEnabled(variant.host())) {
                return;
            }
            for (var id : List.of(variant.ore().stoneOre(), variant.ore().deepslateOre())) {
                BuiltInRegistries.BLOCK.getOptional(id).ifPresent(ore ->
                        byOre.computeIfAbsent(ore, o -> new ArrayList<>()).add(Map.entry(stone, block)));
            }
        });
        if (byOre.isEmpty()) {
            Constants.LOG.info("{}: no supported stone is installed and switched on, nothing to do", NAME);
            return;
        }

        final Registry<Feature> features = registries.lookupOrThrow(Registries.FEATURE);
        int patched = 0;
        int added = 0;
        for (Holder.Reference<Feature> holder : features.listElements().toList()) {
            if (!(holder.value() instanceof AbstractOreFeature ore)) {
                continue;
            }
            final List<BlockReplacement> extra = new ArrayList<>();
            for (BlockReplacement target : ore.targetStates()) {
                for (Map.Entry<Block, Block> pair : byOre.getOrDefault(target.state().getBlock(), List.of())) {
                    final RuleTest test = RuleTest.allOf(target.target(), new BlockMatchTest(pair.getKey()));
                    extra.add(new BlockReplacement(test, pair.getValue().defaultBlockState()));
                }
            }
            if (extra.isEmpty() || !OreFeatures.rebuildable(holder.value(), NAME)
                    || OreFeatures.placesAny(ore.targetStates(), ours)) {
                continue;
            }
            OreFeatures.prepend(holder, ore, extra);
            patched++;
            added += extra.size();
        }
        Constants.LOG.info("{}: added {} ore targets across {} ore features", NAME, added, patched);
    }
}
