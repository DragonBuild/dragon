//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <Foundation/NSOperation.h>

@class HMCameraClip;

@interface HFCameraClipFeedbackPreparationOperation : NSOperation
{
    HMCameraClip *_cameraClip;
    id /* CDUnknownBlockType */ _completionHandler;
}

@property(copy, nonatomic) id /* CDUnknownBlockType */ completionHandler; // @synthesize completionHandler=_completionHandler;
@property(retain, nonatomic) HMCameraClip *cameraClip; // @synthesize cameraClip=_cameraClip;
// - (void).cxx_destruct;
- (void)main;
- (id)initWithCameraClip:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;

@end
