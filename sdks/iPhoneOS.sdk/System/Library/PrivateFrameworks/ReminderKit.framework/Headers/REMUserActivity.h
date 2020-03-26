//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>


@class NSData;

@interface REMUserActivity : NSObject <NSCopying, NSSecureCoding>
{
    long long _type;
    NSData *_storage;
}

+ (id)stringForActivityType:(long long)arg1;
+ (id)dataFromUserActivity:(id)arg1;
+ (id)userActivityWithDictionaryData:(id)arg1 error:(id )arg2;
+ (BOOL)supportsSecureCoding;
+ (void)userActivityWithUserActivity:(id)arg1 completion:(id /* CDUnknownBlockType */)arg2;
@property(readonly, nonatomic) NSData *storage; // @synthesize storage=_storage;
@property(readonly, nonatomic) long long type; // @synthesize type=_type;
// - (void).cxx_destruct;
- (id)debugDescriptionDetails;
- (id)debugDescription;
- (id)siriIntent;
- (id)userActivityData;
- (id)userActivity;
- (id)universalLink;
- (id)archivedDictionaryData;
- (id)initWithCoder:(id)arg1;
- (void)encodeWithCoder:(id)arg1;
- (BOOL)isEqual:(id)arg1;
// - (id)copyWithZone:(_NSZone )arg1;
- (id)initWithSiriIntent:(id)arg1;
- (id)initWithUserActivityData:(id)arg1;
- (id)initWithUserActivity:(id)arg1;
- (id)initWithUniversalLink:(id)arg1;
- (id)initWithType:(long long)arg1 storage:(id)arg2;

@end
