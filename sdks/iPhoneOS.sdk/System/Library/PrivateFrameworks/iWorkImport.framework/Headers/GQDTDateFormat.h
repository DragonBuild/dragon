//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <iWorkImport/GQDNameMappable-Protocol.h>

__attribute__((visibility("hidden")))
@interface GQDTDateFormat : NSObject <GQDNameMappable>
{
    struct __CFString mFormatString;
}

+ (const struct StateSpec )stateForReading;
- (struct __CFString )formatString;
- (void)dealloc;
- (id)initWithFormatString:(struct __CFString )arg1;
- (int)readAttributesFromReader:(struct _xmlTextReader )arg1;

@end
