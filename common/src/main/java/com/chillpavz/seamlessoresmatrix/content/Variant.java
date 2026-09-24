package com.chillpavz.seamlessoresmatrix.content;

import com.chillpavz.seamlessoresmatrix.Constants;
import net.minecraft.resources.Identifier;

/** One host stone x ore pairing, e.g. limestone + iron -> {@code blockus_limestone_iron_ore}. */
public record Variant(HostStone host, OreKind ore) {

    public String path() {
        return host.name() + "_" + ore.id() + "_ore";
    }

    public Identifier id() {
        return Identifier.fromNamespaceAndPath(Constants.MOD_ID, path());
    }

    /** The vanilla block whose strength this variant takes. */
    public Identifier strengthSource() {
        return ore.strengthSource(host.strength());
    }
}
