//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <SpringBoard/SBTestRecipe-Protocol.h>

@class SBHomeGestureParticipant;

@interface SBHomeGestureArbiterRecipe : NSObject <SBTestRecipe>
{
    SBHomeGestureParticipant *_participant;
}

+ (void)load;
@property(retain, nonatomic) SBHomeGestureParticipant *participant; // @synthesize participant=_participant;
// - (void).cxx_destruct;
- (void)handleVolumeDecrease;
- (void)handleVolumeIncrease;
- (id)title;

@end
