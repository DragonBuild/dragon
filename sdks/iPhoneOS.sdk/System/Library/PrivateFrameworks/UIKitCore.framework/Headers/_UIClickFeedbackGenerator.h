//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import "UIFeedbackGenerator.h"


@interface _UIClickFeedbackGenerator : UIFeedbackGenerator <UIFeedbackGeneratorUserInteractionDriven>
{
}

+ (Class)_configurationClass;
- (id)_clickConfiguration;
- (void)userInteractionCancelled;
- (void)userInteractionEnded;
- (void)userInteractionStarted;
- (void)pressedUp;
- (void)pressedDown;
- (id)initWithCoordinateSpace:(id)arg1;

@end
