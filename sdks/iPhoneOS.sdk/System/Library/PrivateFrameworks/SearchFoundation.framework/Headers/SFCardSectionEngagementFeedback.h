//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <SearchFoundation/SFCardSectionFeedback.h>

@class SFPunchout;

@interface SFCardSectionEngagementFeedback : SFCardSectionFeedback
{
    SFPunchout *_destination;
    NSUInteger _triggerEvent;
    NSUInteger _actionCardType;
    NSUInteger _actionTarget;
}

+ (BOOL)supportsSecureCoding;
@property(nonatomic) NSUInteger actionTarget; // @synthesize actionTarget=_actionTarget;
@property(nonatomic) NSUInteger actionCardType; // @synthesize actionCardType=_actionCardType;
@property(nonatomic) NSUInteger triggerEvent; // @synthesize triggerEvent=_triggerEvent;
@property(retain, nonatomic) SFPunchout *destination; // @synthesize destination=_destination;
// - (void).cxx_destruct;
- (void)encodeWithCoder:(id)arg1;
- (id)initWithCoder:(id)arg1;
- (id)initWithCardSection:(id)arg1 destination:(id)arg2 triggerEvent:(NSUInteger)arg3 actionCardType:(NSUInteger)arg4;

@end
