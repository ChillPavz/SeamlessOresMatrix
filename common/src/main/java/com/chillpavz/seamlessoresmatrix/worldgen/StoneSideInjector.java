package com.chillpavz.seamlessoresmatrix.worldgen;

import com.chillpavz.seamlessoresmatrix.Constants;
import com.chillpavz.seamlessoresmatrix.MatrixConfig;
import com.chillpavz.seamlessoresmatrix.content.HostStone;
import com.chillpavz.seamlessoresmatrix.content.MatrixContent;
import com.chillpavz.seamlessoresmatrix.content.OreKind;
import com.chillpavz.seamlessoresmatrix.content.Variant;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.RegistryAccess;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.levelgen.feature.AbstractOreFeature;
import net.minecraft.world.level.levelgen.feature.BlockReplacement;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.structure.templatesystem.BlockMatchTest;
import net.minecraft.world.level.levelgen.structure.templatesystem.RuleTest;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Restyles ore that a modded stone swallowed, by extending the STONE's feature.
 *
 * <h2>Why the stone side</h2>
 * Modded stones are added through biome modifiers and Fabric's biome API, which append, so their blobs
 * are placed after the ores. A blob replaces the rock around an ore and leaves the ore, still wearing
 * stone or deepslate, inside it. That seam is what this fixes.
 *
 * <p>For every ore kind the stone swallows, one replacement is put in front of the stone feature's own
 * targets: {@code any_of(block_match <each form of that ore>) -> <that ore in this stone>}. Where the
 * blob meets an ore, the ore becomes the variant; everywhere else the blob does what it always did. The
 * same positions hold ore, in the same number: one for one, no ore added or removed.
 *
 * <p>The forms of an ore are its stone and deepslate blocks, Seamless Ores' own variants of it when that
 * mod is installed (a limestone blob placed over granite leaves Seamless Ores' granite iron inside
 * limestone), and our variants of it in the other hosts (limestone over marble does the same to ours).
 */
public final class StoneSideInjector {

    static final String NAME = "Stone side";

    /** Seamless Ores' hosts. Its variants are looked up by id, and only used when they exist. */
    private static final String[] SEAMLESS_ORES_HOSTS = {"granite", "diorite", "andesite", "tuff"};

    private StoneSideInjector() {}

    public static void inject(RegistryAccess registries) {

        final Map<Block, Variant> ours = MatrixContent.byBlock();
        // Which host each stone block is, and which of our blocks each host has per ore.
        final Map<Block, HostStone> hostOf = new IdentityHashMap<>();
        final Map<HostStone, Map<OreKind, Block>> variantsOf = new LinkedHashMap<>();
        ours.forEach((block, variant) -> {
            final Block stone = variant.host().block();
            if (stone == null || !MatrixConfig.isEnabled(variant.host())) {
                return;
            }
            hostOf.put(stone, variant.host());
            variantsOf.computeIfAbsent(variant.host(), h -> new EnumMap<>(OreKind.class)).put(variant.ore(), block);
        });
        if (hostOf.isEmpty()) {
            Constants.LOG.info("{}: no supported stone is installed and switched on, nothing to do", NAME);
            return;
        }

        final Registry<Feature> features = registries.lookupOrThrow(Registries.FEATURE);
        int patched = 0;
        int added = 0;
        // Collected first: we rebind while iterating.
        for (Holder.Reference<Feature> holder : features.listElements().toList()) {
            if (!(holder.value() instanceof AbstractOreFeature ore)) {
                continue;
            }
            final Set<HostStone> hosts = new LinkedHashSet<>();
            for (BlockReplacement target : ore.targetStates()) {
                final HostStone host = hostOf.get(target.state().getBlock());
                if (host != null) {
                    hosts.add(host);
                }
            }
            if (hosts.isEmpty() || !OreFeatures.rebuildable(holder.value(), NAME)) {
                continue;
            }
            if (OreFeatures.placesAny(ore.targetStates(), ours)) {
                continue;   // already done, e.g. a second world opened in the same session
            }
            final HostStone host = hosts.iterator().next();
            if (hosts.size() > 1) {
                // Which stone a swallowed ore should take would depend on which target placed the
                // stone at that position, which a block_match cannot see. No known feature does this.
                Constants.LOG.warn("{}: {} places {} stones, using {} for all of them",
                        NAME, holder.key().identifier(), hosts.size(), host);
            }
            final List<BlockReplacement> extra = new ArrayList<>();
            variantsOf.get(host).forEach((kind, block) -> extra.add(
                    new BlockReplacement(formsOf(kind, block, variantsOf), block.defaultBlockState())));
            OreFeatures.prepend(holder, ore, extra);
            patched++;
            added += extra.size();
            Constants.LOG.info("{}: {} ({}) now converts {} ores", NAME, holder.key().identifier(), host,
                    extra.size());
        }
        Constants.LOG.info("{}: prepended {} ore targets across {} stone features", NAME, added, patched);
    }

    /** Every block that is this kind of ore, other than the variant it becomes. */
    private static RuleTest formsOf(OreKind kind, Block becomes, Map<HostStone, Map<OreKind, Block>> variantsOf) {
        final List<RuleTest> tests = new ArrayList<>();
        addIfPresent(tests, kind.stoneOre());
        addIfPresent(tests, kind.deepslateOre());
        for (String host : SEAMLESS_ORES_HOSTS) {
            addIfPresent(tests, Identifier.fromNamespaceAndPath("seamlessores", host + "_" + kind.id() + "_ore"));
        }
        for (Map<OreKind, Block> other : variantsOf.values()) {
            final Block block = other.get(kind);
            if (block != null && block != becomes) {
                tests.add(new BlockMatchTest(block));
            }
        }
        return tests.size() == 1 ? tests.get(0) : RuleTest.anyOf(tests);
    }

    private static void addIfPresent(List<RuleTest> tests, Identifier id) {
        BuiltInRegistries.BLOCK.getOptional(id).ifPresent(block -> tests.add(new BlockMatchTest(block)));
    }
}
