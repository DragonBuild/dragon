//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class NSMutableArray, NSURL, PHMediaFormatConversionJob;
@protocol OS_dispatch_queue, PHMediaFormatConversionImplementation;

@interface PHMediaFormatConversionManager : NSObject
{
    id /* CDUnknownBlockType */ _transferBehaviorUserPreferenceOverride;
    NSURL *_directoryForTemporaryFiles;
    NSUInteger _state;
    NSObject<PHMediaFormatConversionImplementation> *_conversionImplementation;
    NSMutableArray *_queuedJobs;
    PHMediaFormatConversionJob *_currentlyProcessingJob;
    NSObject<OS_dispatch_queue> *_stateQueue;
    NSObject<OS_dispatch_queue> *_callbackQueue;
    NSObject<OS_dispatch_queue> *_preflightQueue;
}

@property(retain) NSObject<OS_dispatch_queue> *preflightQueue; // @synthesize preflightQueue=_preflightQueue;
@property(retain) NSObject<OS_dispatch_queue> *callbackQueue; // @synthesize callbackQueue=_callbackQueue;
@property(retain) NSObject<OS_dispatch_queue> *stateQueue; // @synthesize stateQueue=_stateQueue;
@property(retain) PHMediaFormatConversionJob *currentlyProcessingJob; // @synthesize currentlyProcessingJob=_currentlyProcessingJob;
@property(retain) NSMutableArray *queuedJobs; // @synthesize queuedJobs=_queuedJobs;
@property(retain) NSObject<PHMediaFormatConversionImplementation> *conversionImplementation; // @synthesize conversionImplementation=_conversionImplementation;
@property NSUInteger state; // @synthesize state=_state;
@property(retain, nonatomic) NSURL *directoryForTemporaryFiles; // @synthesize directoryForTemporaryFiles=_directoryForTemporaryFiles;
// - (void).cxx_destruct;
- (id)ut_objectsToBeDeallocatedWithReceiver;
- (void)invalidate;
- (void)cancellationRequestedForJob:(id)arg1;
- (id)jobForConversionRequest:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (id)rootAncestorRequestForRequest:(id)arg1;
- (void)preflightAllRelatedRequestsForCurrentJob;
- (void)validateLivePhotoPairingIdentifierConfigurationForRequest:(id)arg1;
- (void)performConversionRequest:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)processQueuedJobs;
- (void)setTransferBehaviorUserPreferenceOverride:(id /* CDUnknownBlockType */)arg1;
- (void)configureTransferBehaviorUserPreferenceForRequest:(id)arg1;
- (void)preflightConversionRequest:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)preflightConversionRequest:(id)arg1;
- (void)enqueueConversionRequest:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)setupConversionImplementation;
- (id)init;

@end
