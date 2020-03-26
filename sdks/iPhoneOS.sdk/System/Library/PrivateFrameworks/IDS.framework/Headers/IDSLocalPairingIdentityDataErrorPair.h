//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>


@class NSData, NSError;

@interface IDSLocalPairingIdentityDataErrorPair : NSObject <NSSecureCoding>
{
    NSData *_identityData;
    NSError *_error;
}

+ (BOOL)supportsSecureCoding;
@property(retain, nonatomic) NSError *error; // @synthesize error=_error;
@property(retain, nonatomic) NSData *identityData; // @synthesize identityData=_identityData;
// - (void).cxx_destruct;
- (void)encodeWithCoder:(id)arg1;
- (id)initWithCoder:(id)arg1;
- (id)initWithError:(id)arg1;
- (id)initWithIdentityData:(id)arg1;
- (id)initWithIdentityData:(id)arg1 error:(id)arg2;

@end
