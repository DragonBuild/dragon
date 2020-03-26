//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>


@class HKWorkout, NSArray;

@interface HKLocationReadings : NSObject <NSSecureCoding>
{
    BOOL _isSmoothed;
    HKWorkout *_workout;
    NSArray *_allValidLocations;
    NSArray *_inOrderLocationArrays;
    double _averageSpeed;
    double _topSpeed;
    double _bottomSpeed;
}

+ (BOOL)supportsSecureCoding;
@property(readonly, nonatomic) double bottomSpeed; // @synthesize bottomSpeed=_bottomSpeed;
@property(readonly, nonatomic) double topSpeed; // @synthesize topSpeed=_topSpeed;
@property(readonly, nonatomic) double averageSpeed; // @synthesize averageSpeed=_averageSpeed;
@property(readonly, nonatomic) NSArray *inOrderLocationArrays; // @synthesize inOrderLocationArrays=_inOrderLocationArrays;
@property(readonly, nonatomic) NSArray *allValidLocations; // @synthesize allValidLocations=_allValidLocations;
@property(readonly, nonatomic) HKWorkout *workout; // @synthesize workout=_workout;
@property(readonly, nonatomic) BOOL isSmoothed; // @synthesize isSmoothed=_isSmoothed;
// - (void).cxx_destruct;
- (id)initWithCoder:(id)arg1;
- (void)encodeWithCoder:(id)arg1;
- (id)lastObject;
- (id)firstObject;
- (long long)count;
- (void)_filterLocationsByActiveTimePeriod:(id)arg1;
- (void)_calculateSpeeds;
- (id)description;
- (id)debugDescription;
- (id)initWithLocation:(id)arg1 workout:(id)arg2;
- (id)initWithLocations:(id)arg1 workout:(id)arg2 isSmoothed:(BOOL)arg3;

@end
