//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKitCore/_UIStatusBarDataEntry.h>

@class NSString;

@interface _UIStatusBarDataBatteryEntry : _UIStatusBarDataEntry
{
    BOOL _saverModeActive;
    BOOL _prominentlyShowsDetailString;
    long long _capacity;
    long long _state;
    NSString *_detailString;
}

+ (BOOL)supportsSecureCoding;
@property(copy, nonatomic) NSString *detailString; // @synthesize detailString=_detailString;
@property(nonatomic) BOOL prominentlyShowsDetailString; // @synthesize prominentlyShowsDetailString=_prominentlyShowsDetailString;
@property(nonatomic) BOOL saverModeActive; // @synthesize saverModeActive=_saverModeActive;
@property(nonatomic) long long state; // @synthesize state=_state;
@property(nonatomic) long long capacity; // @synthesize capacity=_capacity;
// - (void).cxx_destruct;
- (id)_ui_descriptionBuilder;
- (BOOL)isEqual:(id)arg1;
- (id)initWithCoder:(id)arg1;
- (void)encodeWithCoder:(id)arg1;
// - (id)copyWithZone:(_NSZone )arg1;
- (NSUInteger)hash;

@end
