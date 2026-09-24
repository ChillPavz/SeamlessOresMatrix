package com.chillpavz.seamlessoresmatrix.worldgen;

import com.chillpavz.seamlessoresmatrix.Constants;
import net.minecraft.core.RegistryAccess;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Runs both injectors once the world's registries are loaded and before any chunk is generated.
 *
 * <p>Each one is fenced off: if it throws, the world loads without that half of the mod and the log
 * says so once. A cosmetic mod must never be the reason a world does not open.
 */
public final class MatrixWorldgen {

    private MatrixWorldgen() {}

    private static final Set<String> DISABLED = ConcurrentHashMap.newKeySet();

    public static void inject(RegistryAccess registries) {
        run(StoneSideInjector.NAME, () -> StoneSideInjector.inject(registries));
        run(OreSideInjector.NAME, () -> OreSideInjector.inject(registries));
    }

    private static void run(String name, Runnable injector) {
        if (DISABLED.contains(name)) {
            return;
        }
        try {
            injector.run();
        } catch (Throwable t) {
            DISABLED.add(name);
            Constants.LOG.error("{} injection failed and is disabled for this session;"
                    + " ores in modded stones keep their vanilla look", name, t);
        }
    }
}
