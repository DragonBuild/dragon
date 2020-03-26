//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>


@class NSArray, PKDiscoveryMessagesMetadata;

@interface PKDiscoveryManifest : NSObject <NSSecureCoding>
{
    long long _version;
    NSArray *_rules;
    NSArray *_discoveryItems;
    PKDiscoveryMessagesMetadata *_messagesMetadata;
}

+ (BOOL)supportsSecureCoding;
+ (id)manifestFromURL:(id)arg1;
@property(readonly, nonatomic) PKDiscoveryMessagesMetadata *messagesMetadata; // @synthesize messagesMetadata=_messagesMetadata;
@property(readonly, nonatomic) NSArray *discoveryItems; // @synthesize discoveryItems=_discoveryItems;
@property(readonly, nonatomic) NSArray *rules; // @synthesize rules=_rules;
@property(readonly, nonatomic) long long version; // @synthesize version=_version;
// - (void).cxx_destruct;
- (void)encodeWithCoder:(id)arg1;
- (id)initWithCoder:(id)arg1;
- (id)initWithVersion:(long long)arg1 rules:(id)arg2 discoveryItems:(id)arg3 engagementMessagesMetadata:(id)arg4;
- (id)initWithDictionary:(id)arg1;

@end
