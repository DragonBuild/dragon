//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <IconServices/ISIconResourceLocator.h>


@class NSString;

@interface ISIconTypeResourceLocator : ISIconResourceLocator <NSSecureCoding>
{
    NSString *_type;
}

+ (BOOL)supportsSecureCoding;
@property(readonly) NSString *type; // @synthesize type=_type;
// - (void).cxx_destruct;
- (BOOL)allowLocalizedIcon;
- (id)preferedResourceName;
- (id)bundleIdentifier;
- (id)resourceDirectoryURL;
- (id)initWithCoder:(id)arg1;
- (void)encodeWithCoder:(id)arg1;
- (id)initWithType:(id)arg1;

@end
