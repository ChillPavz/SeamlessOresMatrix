package com.chillpavz.seamlessoresmatrix;

import com.chillpavz.seamlessoresmatrix.config.MatrixConfigData;
import com.chillpavz.seamlessoresmatrix.content.MatrixContent;
import com.chillpavz.seamlessoresmatrix.worldgen.MatrixWorldgen;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

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

        // Worldgen registries are datapack-loaded per world: they exist from here, and no chunk has
        // been generated yet.
        ServerLifecycleEvents.SERVER_STARTING.register(server -> MatrixWorldgen.inject(server.registryAccess()));
    }
}
