//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <RunningBoardServices/BSDescriptionProviding-Protocol.h>
#import <RunningBoardServices/BSXPCSecureCoding-Protocol.h>

@class NSMutableDictionary, NSSet, NSString, RBSProcessHandle;
@protocol OS_xpc_object;

@interface RBSProcessState : NSObject <BSXPCSecureCoding, BSDescriptionProviding, NSCopying>
{
//     struct os_unfair_lock_s _lock;
    NSObject<OS_xpc_object> *_codedState;
    NSUInteger _codedValues;
    NSMutableDictionary *_codedStateCache;
    unsigned char _taskState;
    unsigned char _debugState;
    unsigned char _preventLaunchState;
    unsigned char _terminationResistance;
    RBSProcessHandle *_process;
    NSSet *_endowmentNamespaces;
    NSSet *_tags;
    NSSet *_legacyAssertions;
    NSSet *_primitiveAssertions;
}

+ (BOOL)supportsBSXPCSecureCoding;
+ (void)setActiveStateDescriptor:(id)arg1;
+ (id)stateWithProcess:(id)arg1;
@property(nonatomic) unsigned char terminationResistance; // @synthesize terminationResistance=_terminationResistance;
@property(copy, nonatomic) NSSet *primitiveAssertions; // @synthesize primitiveAssertions=_primitiveAssertions;
@property(copy, nonatomic) NSSet *legacyAssertions; // @synthesize legacyAssertions=_legacyAssertions;
@property(copy, nonatomic) NSSet *tags; // @synthesize tags=_tags;
@property(copy, nonatomic) NSSet *endowmentNamespaces; // @synthesize endowmentNamespaces=_endowmentNamespaces;
@property(nonatomic) unsigned char preventLaunchState; // @synthesize preventLaunchState=_preventLaunchState;
@property(nonatomic) unsigned char debugState; // @synthesize debugState=_debugState;
@property(nonatomic) unsigned char taskState; // @synthesize taskState=_taskState;
@property(readonly, nonatomic) RBSProcessHandle *process; // @synthesize process=_process;
// - (void).cxx_destruct;
// - (id)copyWithZone:(_NSZone )arg1;
- (id)initWithBSXPCCoder:(id)arg1;
- (void)encodeWithBSXPCCoder:(id)arg1;
- (id)descriptionBuilderWithMultilinePrefix:(id)arg1;
- (id)descriptionWithMultilinePrefix:(id)arg1;
- (id)succinctDescriptionBuilder;
- (id)succinctDescription;
@property(readonly, copy) NSString *description;
- (BOOL)isEqual:(id)arg1;
@property(readonly) NSUInteger hash;
- (void)_lock_finalizeCodingForValues:(NSUInteger)arg1;
- (id)_lock_encodedStateForDescriptor:(id)arg1;
- (void)encodeWithPreviousState:(id)arg1;
- (BOOL)isDifferentFromState:(id)arg1 significantly:(out BOOL )arg2;
@property(readonly, copy, nonatomic) NSSet *assertions;
@property(readonly, nonatomic, getter=isPreventedFromLaunching) BOOL preventedFromLaunching;
@property(readonly, nonatomic, getter=isEmptyState) BOOL emptyState;
@property(readonly, nonatomic, getter=isDebugging) BOOL debugging;
@property(readonly, nonatomic, getter=isRunning) BOOL running;
- (id)init;
- (id)initWithProcess:(id)arg1;

@end
