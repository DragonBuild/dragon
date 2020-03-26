//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@interface MCDeviceCapabilities : NSObject
{
    BOOL _supportsBlockLevelEncryption;
    BOOL _supportsFileLevelEncryption;
}

+ (id)currentDevice;
@property(readonly, nonatomic) BOOL supportsFileLevelEncryption; // @synthesize supportsFileLevelEncryption=_supportsFileLevelEncryption;
@property(readonly, nonatomic) BOOL supportsBlockLevelEncryption; // @synthesize supportsBlockLevelEncryption=_supportsBlockLevelEncryption;
- (BOOL)validateCapabilitiesRequiredByRestrictions:(id)arg1 localizedIncompatibilityMessage:(id)arg2 outError:(id )arg3;
- (id)init;
- (BOOL)_mediaDiskIsEncrypted;

@end
