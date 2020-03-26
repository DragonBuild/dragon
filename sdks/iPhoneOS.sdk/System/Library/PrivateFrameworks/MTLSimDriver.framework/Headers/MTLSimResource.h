//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <MTLSimDriver/MTLResourceSPI-Protocol.h>
#import <MTLSimDriver/MTLSerializerResource-Protocol.h>

@class MTLResourceAllocationInfo, MTLSimDevice, MTLSimHeap, NSString;
@protocol MTLDevice, MTLHeap;

__attribute__((visibility("hidden")))
@interface MTLSimResource : NSObject <MTLResourceSPI, MTLSerializerResource>
{
    NSUInteger _purgeableState;
    MTLSimHeap *_heap;
    NSUInteger _heapOffset;
    unsigned int _resourceRef;
    NSUInteger _options;
    NSUInteger _cpuCacheMode;
    NSUInteger _storageMode;
    MTLSimDevice *_device;
    NSString *_label;
//     struct os_unfair_lock_s _labelLock;
    NSUInteger _hazardTrackingMode;
    BOOL _isAliasable;
    int responsibleProcess;
    NSUInteger allocatedSize;
    MTLResourceAllocationInfo *cachedAllocationInfo;
    NSUInteger protectionOptions;
    MTLResourceAllocationInfo *sharedAllocationInfo;
}

@property(readonly) MTLResourceAllocationInfo *sharedAllocationInfo; // @synthesize sharedAllocationInfo;
@property int responsibleProcess; // @synthesize responsibleProcess;
@property(readonly) NSUInteger protectionOptions; // @synthesize protectionOptions;
@property(readonly) MTLResourceAllocationInfo *cachedAllocationInfo; // @synthesize cachedAllocationInfo;
@property(readonly) unsigned int resourceRef; // @synthesize resourceRef=_resourceRef;
@property(readonly) NSUInteger allocatedSize; // @synthesize allocatedSize;
@property(readonly) NSUInteger cpuCacheMode; // @synthesize cpuCacheMode=_cpuCacheMode;
@property(readonly) NSUInteger heapOffset;
- (void)waitUntilComplete;
- (BOOL)isPurgeable;
- (BOOL)isComplete;
- (BOOL)doesAliasResource:(id)arg1;
- (BOOL)doesAliasAnyResources:(const id )arg1 count:(NSUInteger)arg2;
- (BOOL)doesAliasAllResources:(const id )arg1 count:(NSUInteger)arg2;
- (BOOL)doesAliasResources:(const id )arg1 count:(NSUInteger)arg2 all:(BOOL)arg3;
@property(readonly) NSUInteger hazardTrackingMode; // @dynamic hazardTrackingMode;
@property(readonly) NSUInteger unfilteredResourceOptions; // @dynamic unfilteredResourceOptions;
@property(readonly) NSUInteger resourceOptions; // @dynamic resourceOptions;
@property(readonly) NSUInteger storageMode; // @synthesize storageMode=_storageMode;
- (NSUInteger)setPurgeableState:(NSUInteger)arg1;
- (void)makeAliasable;
- (BOOL)isAliasable;
@property(readonly) id <MTLHeap> heap; // @dynamic heap;
@property(copy) NSString *label; // @dynamic label;
- (id)retainedLabel;
@property(readonly) id <MTLDevice> device; // @dynamic device;
- (void)dealloc;
- (id)initWithResourceRef:(unsigned int)arg1 options:(NSUInteger)arg2 device:(id)arg3 heap:(id)arg4;

@end
