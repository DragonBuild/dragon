//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class TXRImageInfo;
@protocol OS_dispatch_semaphore;

__attribute__((visibility("hidden")))
@interface TXRDeferredImageInfo : NSObject
{
    NSObject<OS_dispatch_semaphore> *_infoLoaded;
    TXRImageInfo *_info;
}

@property(retain, nonatomic) TXRImageInfo *info; // @synthesize info=_info;
// - (void).cxx_destruct;
- (void)signalLoaded;
- (id)init;

@end
