package com.chillpavz.seamlessoresmatrix;

import com.chillpavz.seamlessoresmatrix.content.HostStone;

import java.util.HashSet;
import java.util.Set;

/**
 * Plain values holder that worldgen reads.
 *
 * <p>Lives in {@code common} and holds no library types. Cloth Config's annotated class cannot live
 * here, because loader dependencies are not on common's classpath, so each loader module owns its
 * own annotated copy and pushes the values in here through {@link #apply}. Keep the two loader
 * copies identical.
 *
 * <p><b>Config affects worldgen only, never registration.</b> The registered block set is derived
 * from the loaded mod set so a client and a server always agree; if config could add or remove
 * blocks, a mismatch would kick players on join. Switching a stone off only means its variants never
 * generate: the blocks still exist, in the creative tab and in every tag.
 *
 * <p>Changes take effect the next time a world loads, because the injection runs at server start.
 * Already-generated chunks never change either way.
 */
public final class MatrixConfig {

    private MatrixConfig() {}

    /** Host stones whose variants are switched off, by {@link HostStone#name()}. */
    private static volatile Set<String> disabledHosts = Set.of();

    /** One field per setting, assigned by name so two neighbours cannot be swapped silently. */
    public static final class Values {
        public boolean blockusLimestone = true;
        public boolean blockusMarble = true;
        public boolean blockusBluestone = true;
        public boolean blockusViridite = true;
        public boolean wilderwildGabbro = true;
    }

    public static void apply(Values values) {
        final Set<String> off = new HashSet<>();
        disable(off, HostStone.BLOCKUS_LIMESTONE, values.blockusLimestone);
        disable(off, HostStone.BLOCKUS_MARBLE, values.blockusMarble);
        disable(off, HostStone.BLOCKUS_BLUESTONE, values.blockusBluestone);
        disable(off, HostStone.BLOCKUS_VIRIDITE, values.blockusViridite);
        disable(off, HostStone.WILDERWILD_GABBRO, values.wilderwildGabbro);
        disabledHosts = Set.copyOf(off);
        if (!off.isEmpty()) {
            Constants.LOG.info("Config: generation switched off for {}", off);
        }
    }

    private static void disable(Set<String> off, HostStone host, boolean enabled) {
        if (!enabled) {
            off.add(host.name());
        }
    }

    /** Whether this stone's variants are generated. */
    public static boolean isEnabled(HostStone host) {
        return !disabledHosts.contains(host.name());
    }
}
