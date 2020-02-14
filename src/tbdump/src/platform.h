/*
 * Copyright (c) 2016 Siguza
 */

#ifndef PLATFORM_H
#define PLATFORM_H

typedef unsigned char platform_t;

#define PLATFORM_UNKNOWN    ((platform_t)0)
#define PLATFORM_OSX        ((platform_t)1)
#define PLATFORM_IOS        ((platform_t)2)
#define PLATFORM_TVOS       ((platform_t)3)
#define PLATFORM_WATCHOS    ((platform_t)4)

const char* strPlatform(platform_t platform);

#endif
