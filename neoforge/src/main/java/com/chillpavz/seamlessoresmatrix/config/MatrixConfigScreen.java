package com.chillpavz.seamlessoresmatrix.config;

import net.neoforged.fml.ModContainer;
import net.neoforged.neoforge.client.gui.IConfigScreenFactory;

/**
 * Wires the Config button in NeoForge's mods list.
 *
 * <p><b>Client-only</b>, and in its own class so a dedicated server never loads the screen types it
 * names. Only touch it behind a {@code FMLEnvironment.getDist() == Dist.CLIENT} guard.
 */
public final class MatrixConfigScreen {

    private MatrixConfigScreen() {}

    public static void register(ModContainer container) {
        container.registerExtensionPoint(IConfigScreenFactory.class,
                (mod, parent) -> MatrixConfigScreenFactory.create(parent));
    }
}
