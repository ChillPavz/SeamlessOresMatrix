package com.chillpavz.seamlessoresmatrix.config;

import com.chillpavz.seamlessoresmatrix.Constants;
import com.chillpavz.seamlessoresmatrix.MatrixConfig;
import me.shedaniel.autoconfig.AutoConfig;
import me.shedaniel.autoconfig.ConfigData;
import me.shedaniel.autoconfig.annotation.Config;
import me.shedaniel.autoconfig.annotation.ConfigEntry;
import me.shedaniel.autoconfig.serializer.GsonConfigSerializer;
import net.minecraft.world.InteractionResult;

/**
 * Cloth Config data class.
 *
 * <p><b>This file is duplicated VERBATIM in the fabric and neoforge modules, and both copies must stay
 * byte-identical.</b> It cannot live in {@code common} because Cloth is a loader dependency. The
 * values are pushed into {@link MatrixConfig}, which is where the worldgen code reads them.
 *
 * <p>One category per stone mod, named by its mod id so {@link MatrixConfigScreenFactory} can hide
 * the category of a mod that is not installed. Category order is field declaration order; keep the
 * mods alphabetical by display name. Everything here gates generation, never registration.
 */
@Config(name = Constants.MOD_ID)
public class MatrixConfigData implements ConfigData {

    // --- Blockus --------------------------------------------------------------------------------

    @ConfigEntry.Category("blockus")
    @ConfigEntry.Gui.Tooltip
    public boolean blockusLimestone = true;

    @ConfigEntry.Category("blockus")
    @ConfigEntry.Gui.Tooltip
    public boolean blockusMarble = true;

    @ConfigEntry.Category("blockus")
    @ConfigEntry.Gui.Tooltip
    public boolean blockusBluestone = true;

    @ConfigEntry.Category("blockus")
    @ConfigEntry.Gui.Tooltip
    public boolean blockusViridite = true;

    // --- Wilder Wild ----------------------------------------------------------------------------

    @ConfigEntry.Category("wilderwild")
    @ConfigEntry.Gui.Tooltip
    public boolean wilderwildGabbro = true;

    /** Registers the config and wires it to the common holder. Safe on client and dedicated server. */
    public static void register() {
        AutoConfig.register(MatrixConfigData.class, GsonConfigSerializer::new);
        AutoConfig.getConfigHolder(MatrixConfigData.class).registerSaveListener((holder, data) -> {
            data.push();
            return InteractionResult.SUCCESS;
        });
        AutoConfig.getConfigHolder(MatrixConfigData.class).getConfig().push();
    }

    /** Copies these values into the loader-agnostic holder, by name. */
    public void push() {
        final MatrixConfig.Values values = new MatrixConfig.Values();
        values.blockusLimestone = blockusLimestone;
        values.blockusMarble = blockusMarble;
        values.blockusBluestone = blockusBluestone;
        values.blockusViridite = blockusViridite;
        values.wilderwildGabbro = wilderwildGabbro;
        MatrixConfig.apply(values);
    }
}
