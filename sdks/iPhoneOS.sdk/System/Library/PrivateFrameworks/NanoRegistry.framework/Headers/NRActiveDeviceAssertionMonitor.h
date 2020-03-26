//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class NSHashTable;
@protocol OS_dispatch_queue;

@interface NRActiveDeviceAssertionMonitor : NSObject
{
    int _assertionToken;
    NSHashTable *_observers;
    NSObject<OS_dispatch_queue> *_workQueue;
}

+ (id)sharedInstance;
@property(nonatomic) int assertionToken; // @synthesize assertionToken=_assertionToken;
@property(retain, nonatomic) NSObject<OS_dispatch_queue> *workQueue; // @synthesize workQueue=_workQueue;
@property(retain, nonatomic) NSHashTable *observers; // @synthesize observers=_observers;
// - (void).cxx_destruct;
- (void)notifyObserversWithTokenValue:(int)arg1;
- (void)stopObservingToken;
- (void)startObservingToken;
- (void)removeObserver:(id)arg1;
- (void)addObserver:(id)arg1;
@property(readonly, nonatomic) BOOL hasActiveAssertion;
- (id)_init;

@end
