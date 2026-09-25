package com.chillpavz.seamlessoresmatrix;

import com.chillpavz.seamlessoresmatrix.config.MatrixConfigData;
import com.chillpavz.seamlessoresmatrix.content.MatrixContent;
import com.chillpavz.seamlessoresmatrix.content.OreKind;
import com.chillpavz.seamlessoresmatrix.worldgen.MatrixWorldgen;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.resource.v1.ResourceLoader;
import net.fabricmc.fabric.api.resource.v1.pack.PackActivationType;
import net.fabricmc.loader.api.FabricLoader;
import net.fabricmc.loader.api.ModContainer;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

import java.util.Set;
import java.util.TreeSet;

public class SeamlessOresMatrixFabric implements ModInitializer {

    @Override
    public void onInitialize() {

        SeamlessOresMatrix.init();

        // Before worldgen, which reads it at server start. Wrapped: a Cloth that is present but broken
        // leaves the defaults (every stone on) rather than taking the game down.
        try {
            MatrixConfigData.register();
        } catch (Throwable t) {
            Constants.LOG.error("Cloth Config could not be initialised; running with default settings", t);
        }

        MatrixContent.registerBlocks((id, block) -> Registry.register(BuiltInRegistries.BLOCK, id, block));
        MatrixContent.registerItems((id, item) -> Registry.register(BuiltInRegistries.ITEM, id, item));
        MatrixContent.registerCreativeTab((id, tab) -> Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, id, tab));

        // CreativeModeTab.Output is protected, so the tab is filled through the loader's own event.
        CreativeModeTabEvents.modifyOutputEvent(MatrixContent.TAB).register(output -> {
            for (var item : MatrixContent.creativeTabItems()) {
                output.accept(new ItemStack(item), CreativeModeTab.TabVisibility.PARENT_AND_SEARCH_TABS);
            }
        });

        registerOreTagPacks();

        // Worldgen registries are datapack-loaded per world: they exist from here, and no chunk has
        // been generated yet.
        ServerLifecycleEvents.SERVER_STARTING.register(server -> MatrixWorldgen.inject(server.registryAccess()));
    }

    /**
     * Enables each ore mod's c:ores/&lt;material&gt; entries only when that mod is loaded.
     *
     * <p>Fabric's {@code tags_populated} resource condition counts a tag as populated as soon as any
     * file names it, even when every entry in it is optional and absent. A c:ores/tin that only our tin
     * variants filled would let recipes gated on it load in a world without any tin mod, with an
     * ingredient that matches nothing, and some mods crash on those. Fabric applies no conditions to tag
     * files, so each ore mod's entries ship in a built-in data pack of their own,
     * {@code resourcepacks/<modid>/} in this jar, registered here only for mods that are loaded. Always
     * enabled, so existing worlds pick them up too.
     */
    private static void registerOreTagPacks() {
        final ModContainer self = FabricLoader.getInstance().getModContainer(Constants.MOD_ID).orElse(null);
        if (self == null) {
            Constants.LOG.error("Cannot find our own mod container, so no ore material tags are loaded");
            return;
        }
        final Set<String> mods = new TreeSet<>();
        for (OreKind ore : OreKind.values()) {
            if (ore.modId() != null) {
                mods.add(ore.modId());
            }
        }
        for (String modId : mods) {
            if (!FabricLoader.getInstance().isModLoaded(modId) || self.findPath("resourcepacks/" + modId).isEmpty()) {
                continue;
            }
            final String name = FabricLoader.getInstance().getModContainer(modId)
                    .map(container -> container.getMetadata().getName()).orElse(modId);
            try {
                if (!ResourceLoader.registerBuiltinPack(Identifier.fromNamespaceAndPath(Constants.MOD_ID, modId), self,
                        Component.literal("Seamless Ores: Matrix, " + name + " ore tags"),
                        PackActivationType.ALWAYS_ENABLED)) {
                    Constants.LOG.warn("Could not register the {} ore tag pack; its variants miss their c:ores tags", name);
                }
            } catch (Throwable t) {
                Constants.LOG.warn("Could not register the {} ore tag pack; its variants miss their c:ores tags", name, t);
            }
        }
    }
}
