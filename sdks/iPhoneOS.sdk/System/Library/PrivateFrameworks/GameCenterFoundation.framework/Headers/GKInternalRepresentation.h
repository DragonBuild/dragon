//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>


@interface GKInternalRepresentation : NSObject <NSCoding, NSCopying, NSSecureCoding>
{
}

+ (id)secureCodedPropertyKeys;
+ (id)codedPropertyKeys;
+ (id)internalRepresentation;
+ (BOOL)supportsSecureCoding;
- (void)mergePropertiesFrom:(id)arg1;
- (id)serverRepresentation;
- (id)description;
- (id)_gkDescriptionWithChildren:(int)arg1;
- (id)descriptionSubstitutionMap;
// - (id)copyWithZone:(_NSZone )arg1;
- (void)encodeWithCoder:(id)arg1;
- (id)initWithCoder:(id)arg1;

@end
