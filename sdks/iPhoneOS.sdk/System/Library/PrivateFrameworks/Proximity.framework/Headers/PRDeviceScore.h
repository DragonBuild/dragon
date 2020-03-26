//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class NSData, PRAngleMeasurement, PRRangeMeasurement;

@interface PRDeviceScore : NSObject
{
    NSData *_btAddress;
    long long _proximity;
    PRRangeMeasurement *_range;
    PRAngleMeasurement *_angle;
    double _score;
    double _scoreUncertainty;
    double _timestamp;
}

@property(nonatomic) double timestamp; // @synthesize timestamp=_timestamp;
@property(readonly) double scoreUncertainty; // @synthesize scoreUncertainty=_scoreUncertainty;
@property(readonly) double score; // @synthesize score=_score;
@property(readonly) PRAngleMeasurement *angle; // @synthesize angle=_angle;
@property(readonly) PRRangeMeasurement *range; // @synthesize range=_range;
@property(readonly) long long proximity; // @synthesize proximity=_proximity;
@property(readonly) NSData *btAddress; // @synthesize btAddress=_btAddress;
// - (void).cxx_destruct;
- (id)initWithValues:(id)arg1 proximity:(long long)arg2 range:(id)arg3 angle:(id)arg4 score:(double)arg5 scoreUncertainty:(double)arg6;
- (id)init;

@end
