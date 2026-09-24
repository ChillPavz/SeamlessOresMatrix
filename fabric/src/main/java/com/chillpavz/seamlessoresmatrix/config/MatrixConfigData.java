package com.chillpavz.seamlessoresmatrix.config;

import com.chillpavz.seamlessoresmatrix.Constants;
import com.chillpavz.seamlessoresmatrix.MatrixConfig;
import me.shedaniel.autoconfig.AutoConfig;
import me.shedaniel.autoconfig.ConfigData;
import me.shedaniel.autoconfig.annotation.Config;
import me.shedaniel.autoconfig.annotation.ConfigEntry;
import me.shedaniel.autoconfig.serializer.GsonConfigSerializer;
import net.minecraft.world.InteractionResult;

import java.util.LinkedHashMap;
import java.util.Map;

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
 *
 * <p>The switches are GENERATED from the host table by tools/generate_assets.py: one per host stone,
 * named after it, in a category named after the mod that places it. Do not edit them by hand.
 */
@Config(name = Constants.MOD_ID)
public class MatrixConfigData implements ConfigData {

    // BEGIN GENERATED switches (tools/generate_assets.py, from the host table)
    // --- Blockus -------------------------------------------------------------------------------------

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

    // --- Create --------------------------------------------------------------------------------------

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean createAsurine = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean createCrimsite = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean createLimestone = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean createOchrum = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean createScorchia = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean createScoria = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean createVeridium = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean minecraftCalcite = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean minecraftDripstoneBlock = true;

    @ConfigEntry.Category("create")
    @ConfigEntry.Gui.Tooltip
    public boolean minecraftSmoothBasalt = true;

    // --- Forbidden and Arcanus -----------------------------------------------------------------------

    @ConfigEntry.Category("forbidden_arcanus")
    @ConfigEntry.Gui.Tooltip
    public boolean forbiddenArcanusDarkstone = true;

    // --- Mythic Upgrades -----------------------------------------------------------------------------

    @ConfigEntry.Category("mythicupgrades")
    @ConfigEntry.Gui.Tooltip
    public boolean mythicupgradesAquamarineSchist = true;

    @ConfigEntry.Category("mythicupgrades")
    @ConfigEntry.Gui.Tooltip
    public boolean mythicupgradesCitrineSchist = true;

    @ConfigEntry.Category("mythicupgrades")
    @ConfigEntry.Gui.Tooltip
    public boolean mythicupgradesPeridotSchist = true;

    @ConfigEntry.Category("mythicupgrades")
    @ConfigEntry.Gui.Tooltip
    public boolean mythicupgradesTopazSchist = true;

    // --- Promenade -----------------------------------------------------------------------------------

    @ConfigEntry.Category("promenade")
    @ConfigEntry.Gui.Tooltip
    public boolean promenadeAsphalt = true;

    @ConfigEntry.Category("promenade")
    @ConfigEntry.Gui.Tooltip
    public boolean promenadeBlunite = true;

    // --- Wilder Wild ---------------------------------------------------------------------------------

    @ConfigEntry.Category("wilderwild")
    @ConfigEntry.Gui.Tooltip
    public boolean wilderwildGabbro = true;
    // END GENERATED switches

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
        final Map<String, Boolean> values = new LinkedHashMap<>();
        // BEGIN GENERATED push
        values.put("blockus_limestone", blockusLimestone);
        values.put("blockus_marble", blockusMarble);
        values.put("blockus_bluestone", blockusBluestone);
        values.put("blockus_viridite", blockusViridite);
        values.put("create_asurine", createAsurine);
        values.put("create_crimsite", createCrimsite);
        values.put("create_limestone", createLimestone);
        values.put("create_ochrum", createOchrum);
        values.put("create_scorchia", createScorchia);
        values.put("create_scoria", createScoria);
        values.put("create_veridium", createVeridium);
        values.put("minecraft_calcite", minecraftCalcite);
        values.put("minecraft_dripstone_block", minecraftDripstoneBlock);
        values.put("minecraft_smooth_basalt", minecraftSmoothBasalt);
        values.put("forbidden_arcanus_darkstone", forbiddenArcanusDarkstone);
        values.put("mythicupgrades_aquamarine_schist", mythicupgradesAquamarineSchist);
        values.put("mythicupgrades_citrine_schist", mythicupgradesCitrineSchist);
        values.put("mythicupgrades_peridot_schist", mythicupgradesPeridotSchist);
        values.put("mythicupgrades_topaz_schist", mythicupgradesTopazSchist);
        values.put("promenade_asphalt", promenadeAsphalt);
        values.put("promenade_blunite", promenadeBlunite);
        values.put("wilderwild_gabbro", wilderwildGabbro);
        // END GENERATED push
        MatrixConfig.apply(values);
    }
}
