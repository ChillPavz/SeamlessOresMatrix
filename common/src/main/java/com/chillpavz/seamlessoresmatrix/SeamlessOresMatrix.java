package com.chillpavz.seamlessoresmatrix;

import com.chillpavz.seamlessoresmatrix.platform.Services;

// Shared entry point. Code here may only touch vanilla and the libraries vanilla itself uses. Anything
// needing a loader API goes behind Services/IPlatformHelper, or lives in the fabric/ and neoforge/
// modules and is called from their own entry points.
public class SeamlessOresMatrix {

    public static void init() {

        Constants.LOG.info("{} initialising on {} ({} environment)", Constants.MOD_NAME,
                Services.PLATFORM.getPlatformName(), Services.PLATFORM.getEnvironmentName());
    }
}
