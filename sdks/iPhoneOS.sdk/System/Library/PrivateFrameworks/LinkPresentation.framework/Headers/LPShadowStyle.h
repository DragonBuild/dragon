//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class UIColor;

__attribute__((visibility("hidden")))
@interface LPShadowStyle : NSObject
{
    double _radius;
    double _opacity;
    UIColor *_color;
}

+ (id)cardHeadingIconShadow;
@property(retain, nonatomic) UIColor *color; // @synthesize color=_color;
@property(nonatomic) double opacity; // @synthesize opacity=_opacity;
@property(nonatomic) double radius; // @synthesize radius=_radius;
// - (void).cxx_destruct;
- (id)init;

@end
