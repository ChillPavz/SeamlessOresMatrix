package com.chillpavz.seamlessoresmatrix;

import com.chillpavz.seamlessoresmatrix.config.MatrixConfigData;
import com.chillpavz.seamlessoresmatrix.config.MatrixConfigScreen;
import com.chillpavz.seamlessoresmatrix.content.MatrixContent;
import com.chillpavz.seamlessoresmatrix.worldgen.MatrixWorldgen;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.loading.FMLEnvironment;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.event.server.ServerAboutToStartEvent;
import net.neoforged.neoforge.registries.RegisterEvent;

@Mod(Constants.MOD_ID)
public class SeamlessOresMatrixNeoForge {

    public SeamlessOresMatrixNeoForge(IEventBus eventBus, ModContainer container) {

        SeamlessOresMatrix.init();

        // Before worldgen, which reads it at server start. Wrapped: a Cloth that is present but broken
        // leaves the defaults (every stone on) rather than taking the game down.
        try {
            MatrixConfigData.register();
            // The screen class names GUI types, so a dedicated server must never load it.
            if (FMLEnvironment.getDist() == Dist.CLIENT) {
                MatrixConfigScreen.register(container);
            }
        } catch (Throwable t) {
            Constants.LOG.error("Cloth Config could not be initialised; running with default settings", t);
        }

        eventBus.addListener(this::onRegister);
        // A MOD bus event. Putting it on the game bus fails silently.
        eventBus.addListener(this::onBuildCreativeTabs);
        // A GAME bus event: the world's registries are loaded and no chunk has been generated yet.
        NeoForge.EVENT_BUS.addListener(this::onServerAboutToStart);
    }

    private void onServerAboutToStart(ServerAboutToStartEvent event) {
        MatrixWorldgen.inject(event.getServer().registryAccess());
    }

    private void onRegister(RegisterEvent event) {
        // Fired once per registry; each call only runs for its own.
        event.register(Registries.BLOCK, helper -> MatrixContent.registerBlocks(helper::register));
        event.register(Registries.ITEM, helper -> MatrixContent.registerItems(helper::register));
        event.register(Registries.CREATIVE_MODE_TAB, helper -> MatrixContent.registerCreativeTab(helper::register));
    }

    private void onBuildCreativeTabs(BuildCreativeModeTabContentsEvent event) {
        if (!event.getTabKey().equals(MatrixContent.TAB)) {
            return;
        }
        for (var item : MatrixContent.creativeTabItems()) {
            event.accept(new ItemStack(item), CreativeModeTab.TabVisibility.PARENT_AND_SEARCH_TABS);
        }
    }
}
