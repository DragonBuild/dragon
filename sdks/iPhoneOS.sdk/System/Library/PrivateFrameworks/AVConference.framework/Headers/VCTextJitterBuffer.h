//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@protocol OS_dispatch_source;

__attribute__((visibility("hidden")))
@interface VCTextJitterBuffer : NSObject
{
    struct tagVCTextJitterBufferConfiguration _configuration;
    BOOL _resetRequested;
    id _delegate;
    struct JitterPreloadQueue_t _preloadQueue;
    struct JitterQueue_t _jitterQueue;
    NSObject<OS_dispatch_source> *_heartbeat;
    unsigned int _lastSequenceNumber;
    BOOL _firstFrameReceived;
}

- (void)heartbeat;
- (void)stopHeartbeat;
- (BOOL)startHeartbeat;
- (void)jitterQueuePushPacket:(struct tagAudioPacket )arg1;
- (void)enqueuePacket:(struct tagAudioPacket )arg1;
- (void)stop;
- (BOOL)start;
- (void)releaseTextFrame:(struct tagAudioFrame )arg1;
- (struct tagAudioFrame )allocTextFrame;
- (void)releaseTextPacket:(struct tagAudioPacket )arg1;
- (struct tagAudioPacket )allocTextPacket;
- (void)setDelegate:(id)arg1;
- (id)delegate;
- (void)dealloc;
- (id)initWithConfiguration:(struct tagVCTextJitterBufferConfiguration )arg1;

@end
