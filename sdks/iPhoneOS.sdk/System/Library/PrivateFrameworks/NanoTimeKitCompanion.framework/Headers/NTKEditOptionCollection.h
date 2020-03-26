//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class NSArray, NSString;

@interface NTKEditOptionCollection : NSObject
{
    long long _mode;
    NSString *_localizedName;
    NSArray *_options;
    NSUInteger _collectionType;
}

+ (id)editOptionCollectionWithEditMode:(long long)arg1 localizedName:(id)arg2 options:(id)arg3 collectionType:(NSUInteger)arg4;
@property(nonatomic) NSUInteger collectionType; // @synthesize collectionType=_collectionType;
@property(copy, nonatomic) NSArray *options; // @synthesize options=_options;
@property(copy, nonatomic) NSString *localizedName; // @synthesize localizedName=_localizedName;
@property(nonatomic) long long mode; // @synthesize mode=_mode;
// - (void).cxx_destruct;
- (BOOL)isEqual:(id)arg1;
- (id)filteredCollectionForDevice:(id)arg1;
- (id)filteredCollectionWithObjectsPassingTest:(id /* CDUnknownBlockType */)arg1;
- (id)initWithEditMode:(long long)arg1 localizedName:(id)arg2 options:(id)arg3 collectionType:(NSUInteger)arg4;
@property(readonly, nonatomic) NSString *optionsDescription;
@property(readonly, nonatomic) long long swatchStyle;

@end
