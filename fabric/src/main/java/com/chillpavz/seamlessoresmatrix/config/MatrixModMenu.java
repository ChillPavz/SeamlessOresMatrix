package com.chillpavz.seamlessoresmatrix.config;

import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import com.terraformersmc.modmenu.api.ModMenuApi;

/**
 * Supplies the config button in Mod Menu's mod list. Mod Menu is optional: this class is only ever
 * loaded by Mod Menu itself, through the {@code modmenu} entrypoint.
 */
public class MatrixModMenu implements ModMenuApi {

    @Override
    public ConfigScreenFactory<?> getModConfigScreenFactory() {
        return MatrixConfigScreenFactory::create;
    }
}
