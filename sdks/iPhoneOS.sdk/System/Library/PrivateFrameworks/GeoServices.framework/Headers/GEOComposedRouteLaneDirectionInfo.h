//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>


@interface GEOComposedRouteLaneDirectionInfo : NSObject <NSSecureCoding>
{
    int _direction;
    float _angle;
}

+ (BOOL)supportsSecureCoding;
@property(readonly, nonatomic) float angle;
@property(readonly, nonatomic) int direction;
- (void)encodeWithCoder:(id)arg1;
- (id)initWithCoder:(id)arg1;
- (id)initWithLaneArrowHead:(id)arg1;

@end
