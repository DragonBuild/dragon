//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class NSOperationQueue;

@interface RCAsyncSerialQueue : NSObject
{
    NSOperationQueue *_serialOperationQueue;
}

@property(retain, nonatomic) NSOperationQueue *serialOperationQueue; // @synthesize serialOperationQueue=_serialOperationQueue;
// - (void).cxx_destruct;
@property(nonatomic) BOOL suspended;
- (void)cancelAllBlocks;
- (void)enqueueOperation:(id)arg1;
- (void)withQualityOfService:(long long)arg1 enqueueBlockForMainThread:(id /* CDUnknownBlockType */)arg2;
- (void)enqueueBlockForMainThread:(id /* CDUnknownBlockType */)arg1;
- (void)enqueueBlock:(id /* CDUnknownBlockType */)arg1;
- (id)initWithQualityOfService:(long long)arg1;
- (id)init;

@end
