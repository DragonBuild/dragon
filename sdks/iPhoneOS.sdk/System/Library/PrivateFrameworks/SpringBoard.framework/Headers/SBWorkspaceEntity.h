//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <SpringBoard/BSDescriptionProviding-Protocol.h>
#import <SpringBoard/SBActivationSettings-Protocol.h>
#import <SpringBoard/SBDeactivationSettings-Protocol.h>
#import <SpringBoard/SBLayoutElementDescriptor-Protocol.h>

@class NSString, SBActivationSettings, SBDeactivationSettings;

@interface SBWorkspaceEntity : NSObject <NSCopying, SBActivationSettings, SBDeactivationSettings, BSDescriptionProviding, SBLayoutElementDescriptor>
{
    NSString *_identifier;
    long long _layoutRole;
    SBActivationSettings *_activationSettings;
    SBDeactivationSettings *_deactivationSettings;
    long long __mainDisplayPreferredInterfaceOrientation;
}

+ (id)entity;
@property(nonatomic, getter=_mainDisplayPreferredInterfaceOrientation, setter=_setMainDisplayPreferredInterfaceOrientation:) long long _mainDisplayPreferredInterfaceOrientation; // @synthesize _mainDisplayPreferredInterfaceOrientation=__mainDisplayPreferredInterfaceOrientation;
@property(readonly, nonatomic) SBDeactivationSettings *deactivationSettings; // @synthesize deactivationSettings=_deactivationSettings;
@property(readonly, nonatomic) SBActivationSettings *activationSettings; // @synthesize activationSettings=_activationSettings;
@property(nonatomic) long long layoutRole; // @synthesize layoutRole=_layoutRole;
// - (void).cxx_destruct;
- (BOOL)hasLayoutAttributes:(NSUInteger)arg1;
- (BOOL)supportsLayoutRole:(long long)arg1;
@property(readonly, copy, nonatomic) id /* CDUnknownBlockType */ entityGenerator;
@property(readonly, nonatomic) Class viewControllerClass;
@property(readonly, nonatomic) NSUInteger layoutAttributes;
@property(readonly, nonatomic) NSUInteger supportedLayoutRoles;
@property(readonly, copy, nonatomic) NSString *uniqueIdentifier;
- (id)descriptionBuilderWithMultilinePrefix:(id)arg1;
- (id)descriptionWithMultilinePrefix:(id)arg1;
- (id)succinctDescriptionBuilder;
- (id)succinctDescription;
// - (id)copyWithZone:(_NSZone )arg1;
- (id /* CDUnknownBlockType */)_generator;
- (BOOL)_supportsLayoutRole:(long long)arg1;
@property(readonly, copy) NSString *description;
- (void)setPreferredInterfaceOrientation:(long long)arg1 onDisplayWithIdentity:(id)arg2;
- (long long)preferredInterfaceOrientationOnDisplayWithIdentity:(id)arg1;
- (BOOL)isAnalogousToEntity:(id)arg1;
@property(readonly, nonatomic) BOOL wantsExclusiveForeground;
@property(readonly, nonatomic) BOOL supportsPresentationAtAnySize;
- (void)clearDeactivationSettings;
- (void)applyDeactivationSettings:(id)arg1;
- (id)copyDeactivationSettings;
- (id)objectForDeactivationSetting:(unsigned int)arg1;
- (void)setObject:(id)arg1 forDeactivationSetting:(unsigned int)arg2;
- (BOOL)boolForDeactivationSetting:(unsigned int)arg1;
- (long long)flagForDeactivationSetting:(unsigned int)arg1;
- (void)setFlag:(long long)arg1 forDeactivationSetting:(unsigned int)arg2;
- (void)clearActivationSettings;
- (void)applyActivationSettings:(id)arg1;
- (id)copyActivationSettings;
- (id)objectForActivationSetting:(unsigned int)arg1;
- (void)setObject:(id)arg1 forActivationSetting:(unsigned int)arg2;
- (BOOL)boolForActivationSetting:(unsigned int)arg1;
- (long long)flagForActivationSetting:(unsigned int)arg1;
- (void)setFlag:(long long)arg1 forActivationSetting:(unsigned int)arg2;
- (id)initWithIdentifier:(id)arg1 displayChangeSettings:(id)arg2;
- (id)init;
- (id)deviceApplicationSceneEntity;
- (BOOL)isDeviceApplicationSceneEntity;
@property(readonly, nonatomic) BOOL isPreviousWorkspaceEntity;
@property(readonly, nonatomic) BOOL isEmptyWorkspaceEntity;
@property(readonly, nonatomic) BOOL isHomeScreenEntity;
- (id)applicationSceneEntity;
- (BOOL)isApplicationSceneEntity;
- (id)inlineAppExposeWorkspaceEntity;
- (BOOL)isInlineAppExposeWorkspaceEntity;

@end
