//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

__attribute__((visibility("hidden")))
@interface OABDrawable : NSObject
{
}

+ (id)readDrawableFromZipPackageData:(const struct CsData )arg1 foundInObject:(id)arg2 state:(id)arg3;
+ (void)setUpXmlDrawingState:(id)arg1 withBinaryReaderState:(id)arg2 targetDocument:(id)arg3 colorMap:(id)arg4;
+ (id)readDrawablesFromContainer:(id)arg1 state:(id)arg2;
+ (id)readDrawableFromObject:(id)arg1 state:(id)arg2;

@end
