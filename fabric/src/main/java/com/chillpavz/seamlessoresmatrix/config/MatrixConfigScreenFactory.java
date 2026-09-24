package com.chillpavz.seamlessoresmatrix.config;

import com.chillpavz.seamlessoresmatrix.Constants;
import com.chillpavz.seamlessoresmatrix.content.HostStone;
import me.shedaniel.autoconfig.AutoConfigClient;
import me.shedaniel.autoconfig.gui.ConfigScreenProvider;
import me.shedaniel.clothconfig2.api.ConfigBuilder;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

import java.util.LinkedHashSet;
import java.util.Set;
import java.util.function.Supplier;

/**
 * Builds the config screen, showing only the stone mods actually installed.
 *
 * <p><b>This file is duplicated VERBATIM in the fabric and neoforge modules, and both copies must stay
 * byte-identical.</b> It is <b>client-only</b>: it names {@code Screen}, so it must only be reached
 * from a client-side hook.
 *
 * <p>Hiding is display only. The field stays in the config file and keeps being pushed, so removing
 * a mod and putting it back does not reset its settings. The mod list comes from
 * {@link HostStone#ALL}, so the screen cannot drift from the stones that exist; a category is named
 * after its mod id.
 */
public final class MatrixConfigScreenFactory {

    private MatrixConfigScreenFactory() {}

    /** AutoConfig's own key shape, so these match the categories it created. */
    private static final String CATEGORY_PREFIX = "text.autoconfig." + Constants.MOD_ID + ".category.";

    /** The config screen to open, given whatever screen the player came from. */
    public static Screen create(Screen parent) {
        final Supplier<Screen> supplier = AutoConfigClient.getConfigScreen(MatrixConfigData.class, parent);

        // A Cloth that stops returning the provider keeps its default screen with every category.
        if (supplier instanceof ConfigScreenProvider<?> provider) {
            provider.setBuildFunction(builder -> {
                hideCategoriesOfAbsentMods(builder);
                return builder.build();
            });
        }
        return supplier.get();
    }

    /**
     * Drops the category of every stone mod that is not installed.
     *
     * <p>Cloth's fallback category is the first one declared, and removing it leaves none: build()
     * then throws, and the Config button with it. So the first category still showing becomes the
     * fallback. With no stone mod installed nothing is hidden, because Cloth cannot show zero
     * categories.
     */
    private static void hideCategoriesOfAbsentMods(ConfigBuilder builder) {
        final Set<String> present = new LinkedHashSet<>();
        final Set<String> absent = new LinkedHashSet<>();
        for (HostStone host : HostStone.ALL) {
            (host.isLoaded() ? present : absent).add(host.modId());
        }
        absent.removeAll(present);
        if (present.isEmpty()) {
            return;
        }
        for (String modId : absent) {
            builder.removeCategoryIfExists(category(modId));
        }
        builder.setFallbackCategory(builder.getOrCreateCategory(category(present.iterator().next())));
    }

    private static Component category(String modId) {
        return Component.translatable(CATEGORY_PREFIX + modId);
    }
}
