//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class NSMutableDictionary;
@protocol OS_dispatch_queue, OS_xpc_object;

@interface MRXPCConnection : NSObject
{
    NSObject<OS_dispatch_queue> *_serialQueue;
    NSMutableDictionary *_customXpcHandlers;
    NSObject<OS_xpc_object> *_connection;
    id /* CDUnknownBlockType */ _messageHandler;
    id /* CDUnknownBlockType */ _invalidationHandler;
}

@property(copy, nonatomic) id /* CDUnknownBlockType */ invalidationHandler; // @synthesize invalidationHandler=_invalidationHandler;
@property(copy, nonatomic) id /* CDUnknownBlockType */ messageHandler; // @synthesize messageHandler=_messageHandler;
@property(readonly, nonatomic) NSObject<OS_xpc_object> *connection; // @synthesize connection=_connection;
// - (void).cxx_destruct;
- (void)_registerCallbacks;
- (id)sendSyncMessage:(id)arg1 error:(id )arg2;
- (void)sendMessage:(id)arg1 queue:(id)arg2 reply:(id /* CDUnknownBlockType */)arg3;
- (void)sendMessageWithType:(NSUInteger)arg1 queue:(id)arg2 reply:(id /* CDUnknownBlockType */)arg3;
- (void)removeCustomXPCHandler:(NSUInteger)arg1;
- (void)addCustomXPCHandler:(id /* CDUnknownBlockType */)arg1 forKey:(NSUInteger)arg2;
@property(readonly, nonatomic) int pid;
- (void)dealloc;
- (id)initWithConnection:(id)arg1 queue:(id)arg2;

@end
