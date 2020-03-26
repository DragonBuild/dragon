//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <CarPlaySupport/CPSTemplateInstanceDelegate-Protocol.h>

@class NSMutableDictionary;
@protocol OS_dispatch_queue;

@interface CPSTemplateConnectionManager : NSObject <CPSTemplateInstanceDelegate>
{
    NSObject<OS_dispatch_queue> *_viewControllerAccessQueue;
    NSMutableDictionary *_viewControllersBySceneIdentifier;
    NSMutableDictionary *_templateInstancesBySceneIdentifier;
}

// - (void).cxx_destruct;
- (id)_listenerEndpointForTestSceneIdentifier:(id)arg1;
- (void)didDisconnectTemplateInstance:(id)arg1;
- (void)updateTemplateInstanceForScene:(id)arg1;
- (id)viewControllerForSceneIdentifierCreateIfNecessary:(id)arg1;
- (BOOL)handleEndpointRequestAction:(id)arg1 forSceneIdentifier:(id)arg2;
- (id)_instanceForSceneIdentifier:(id)arg1;
- (id)init;

@end
