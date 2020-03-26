//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@protocol OS_dispatch_queue;

__attribute__((visibility("hidden")))
@interface ReachabilityCallbacker : NSObject
{
    function_d3afe2e2 _listener;
    NSObject<OS_dispatch_queue> *_queue;
    struct mutex _lock;
}

- (id).cxx_construct;
// - (void).cxx_destruct;
- (void)_reachabilityChanged:(id)arg1;
- (void)clearListener;
- (void)dealloc;
- (id)initWithListener:(function_d3afe2e2)arg1 queue:(id)arg2;

@end
