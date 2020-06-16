/*
 * Copyright (c) 2016 Siguza
 */

#include "platform.h"

const char* strPlatform(platform_t platform)
{
    switch(platform)
    {
        case PLATFORM_OSX:      return "macosx";
        case PLATFORM_IOS:      return "ios";
        case PLATFORM_TVOS:     return "tvos";
        case PLATFORM_WATCHOS:  return "watchos";
    }
    return "unknown";
}
