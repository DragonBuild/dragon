//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <CoreSpeech/CSAudioStreamProvidingDelegate-Protocol.h>
#import <CoreSpeech/NviAudioDataSource-Protocol.h>

@class CSAudioStream, NSHashTable, NviContext;
@protocol OS_dispatch_queue;

@interface NviCSAudioDataSource : NSObject <CSAudioStreamProvidingDelegate, NviAudioDataSource>
{
    NviContext *_nviCtx;
    NSHashTable *_receivers;
    CSAudioStream *_audioStream;
    NSObject<OS_dispatch_queue> *_queue;
}

@property(retain, nonatomic) NSObject<OS_dispatch_queue> *queue; // @synthesize queue=_queue;
@property(retain, nonatomic) CSAudioStream *audioStream; // @synthesize audioStream=_audioStream;
@property(retain, nonatomic) NSHashTable *receivers; // @synthesize receivers=_receivers;
@property(retain, nonatomic) NviContext *nviCtx; // @synthesize nviCtx=_nviCtx;
// - (void).cxx_destruct;
- (void)audioStreamProvider:(id)arg1 audioChunkForTVAvailable:(id)arg2;
- (void)audioStreamProvider:(id)arg1 didStopStreamUnexpectly:(long long)arg2;
- (void)audioStreamProvider:(id)arg1 avBufferAvailable:(id)arg2;
- (void)audioStreamProvider:(id)arg1 audioBufferAvailable:(id)arg2;
- (void)_createAudioStreamWithCurrentNviContext;
- (void)stopWithDidStopHandler:(id /* CDUnknownBlockType */)arg1;
- (void)startWithNviContext:(id)arg1 didStartHandler:(id /* CDUnknownBlockType */)arg2;
- (void)removeReceiver:(id)arg1;
- (void)addReceiver:(id)arg1;
@property(readonly, nonatomic) NSUInteger sampleRate;
@property(readonly, nonatomic) NSUInteger numBytesPerSample;
@property(readonly, nonatomic) NSUInteger type;
- (id)init;

@end
