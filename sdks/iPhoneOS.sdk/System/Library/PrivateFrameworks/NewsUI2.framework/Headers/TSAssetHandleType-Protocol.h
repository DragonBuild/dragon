//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

@class NSString, OS_dispatch_group, UIImage;
@protocol TSAssetDataProviderType;

@protocol TSAssetHandleType
- (void)downloadWithGroup:(OS_dispatch_group *)arg1;
@property(nonatomic, readonly) NSString *uniqueKey;
@property(nonatomic, readonly) UIImage *fallbackImage;
@property(nonatomic, readonly) NSString *filePath;

@optional
@property(nonatomic, readonly) id <TSAssetDataProviderType> assetDataProvider;
@end
