//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <PhotosUICore/PXObservable.h>

@class NSArray, NSDictionary, PXPhotosDataSource;

@interface PXPhotosDataSourceStressTest : PXObservable
{
    BOOL _isPrepared;
    NSArray *_categories;
    NSDictionary *_assetsByCategory;
    NSUInteger _sampleLength;
    NSUInteger _sampleIndex;
    BOOL _running;
    NSUInteger _maximumAssetCount;
    double _updateInterval;
    PXPhotosDataSource *_dataSource;
    NSUInteger _dataSourceIndex;
}

@property(nonatomic, setter=_setDataSourceIndex:) NSUInteger dataSourceIndex; // @synthesize dataSourceIndex=_dataSourceIndex;
@property(retain, nonatomic, setter=_setDataSource:) PXPhotosDataSource *dataSource; // @synthesize dataSource=_dataSource;
@property(nonatomic, getter=isRunning) BOOL running; // @synthesize running=_running;
@property(nonatomic) double updateInterval; // @synthesize updateInterval=_updateInterval;
@property(nonatomic) NSUInteger maximumAssetCount; // @synthesize maximumAssetCount=_maximumAssetCount;
// - (void).cxx_destruct;
- (id)mutableChangeObject;
- (void)_updateDataSource;
- (id)_categoryForAsset:(id)arg1;
- (void)_prepare;
- (id)init;

@end
