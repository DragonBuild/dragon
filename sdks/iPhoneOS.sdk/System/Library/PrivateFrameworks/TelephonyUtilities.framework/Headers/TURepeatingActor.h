//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class TURepeatingAction;
@protocol OS_dispatch_queue;

@interface TURepeatingActor : NSObject
{
    BOOL _stopped;
    BOOL _currentlyPerformingAction;
    NSObject<OS_dispatch_queue> *_queue;
    TURepeatingAction *_currentRepeatingAction;
    TURepeatingAction *_pendingRepeatingAction;
    id /* CDUnknownBlockType */ _attemptNextIterationBlock;
}

@property(copy, nonatomic) id /* CDUnknownBlockType */ attemptNextIterationBlock; // @synthesize attemptNextIterationBlock=_attemptNextIterationBlock;
@property(retain, nonatomic) TURepeatingAction *pendingRepeatingAction; // @synthesize pendingRepeatingAction=_pendingRepeatingAction;
@property(retain, nonatomic) TURepeatingAction *currentRepeatingAction; // @synthesize currentRepeatingAction=_currentRepeatingAction;
@property(nonatomic, getter=isCurrentlyPerformingAction) BOOL currentlyPerformingAction; // @synthesize currentlyPerformingAction=_currentlyPerformingAction;
@property(nonatomic, getter=isStopped) BOOL stopped; // @synthesize stopped=_stopped;
@property(retain, nonatomic) NSObject<OS_dispatch_queue> *queue; // @synthesize queue=_queue;
// - (void).cxx_destruct;
- (void)_completeWithDidFinish:(BOOL)arg1;
- (void)_stopWithDidFinish:(BOOL)arg1;
- (BOOL)_hasIterationsRemaining;
- (void)_attemptNextIteration;
- (void)_beginRepeatingAction:(id)arg1;
@property(readonly, nonatomic, getter=isRunning) BOOL running;
- (void)stop;
- (void)beginRepeatingAction:(id /* CDUnknownBlockType */)arg1 iterations:(NSUInteger)arg2 pauseDurationBetweenIterations:(double)arg3 completion:(id /* CDUnknownBlockType */)arg4;
- (void)beginRepeatingAction:(id /* CDUnknownBlockType */)arg1 iterations:(NSUInteger)arg2 completion:(id /* CDUnknownBlockType */)arg3;
- (id)init;

@end
