//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <VoiceShortcuts/VCSyncDataEndpoint-Protocol.h>

@class NSMutableSet, NSSet, VCDaemonXPCEventHandler;
@protocol OS_dispatch_queue, VCDatabaseProvider;

@interface VCDaemonSyncDataEndpoint : NSObject <VCSyncDataEndpoint>
{
    NSObject<OS_dispatch_queue> *_queue;
    id <VCDatabaseProvider> _databaseProvider;
    VCDaemonXPCEventHandler *_eventHandler;
    NSMutableSet *_mutableSyncDataHandlers;
}

@property(readonly, nonatomic) NSMutableSet *mutableSyncDataHandlers; // @synthesize mutableSyncDataHandlers=_mutableSyncDataHandlers;
@property(readonly, nonatomic) VCDaemonXPCEventHandler *eventHandler; // @synthesize eventHandler=_eventHandler;
@property(readonly, nonatomic) id <VCDatabaseProvider> databaseProvider; // @synthesize databaseProvider=_databaseProvider;
@property(readonly, nonatomic) NSObject<OS_dispatch_queue> *queue; // @synthesize queue=_queue;
// - (void).cxx_destruct;
@property(readonly, nonatomic) NSSet *syncDataHandlers;
- (id)initWithDatabaseProvider:(id)arg1 eventHandler:(id)arg2;

@end
