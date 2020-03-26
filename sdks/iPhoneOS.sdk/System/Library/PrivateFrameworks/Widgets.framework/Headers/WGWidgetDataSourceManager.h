//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <Widgets/WGWidgetVisibilityDelegate-Protocol.h>
#import <Widgets/_WGDataSourceManager-Protocol.h>

@class NSArray, WGWidgetDataSource, WGWidgetVisibilityManager;
@protocol _WGParentDataSourceManager;

@interface WGWidgetDataSourceManager : NSObject <WGWidgetVisibilityDelegate, _WGDataSourceManager>
{
    WGWidgetDataSource *_widgetDataSource;
    WGWidgetVisibilityManager *_widgetVisbilityManager;
    id _plugInDiscoveryToken;
    BOOL _isPublishing;
    id /* CDUnknownBlockType */ _didStartBlock;
    id <_WGParentDataSourceManager> _parentDataSourceManager;
}

+ (id)discoverAvailableWidgetsWithError:(id )arg1;
+ (id)_widgetExtensionsDiscoveryAttributes;
@property(retain, nonatomic, getter=_widgetVisbilityManager) WGWidgetVisibilityManager *widgetVisbilityManager; // @synthesize widgetVisbilityManager=_widgetVisbilityManager;
@property(nonatomic) id <_WGParentDataSourceManager> parentDataSourceManager; // @synthesize parentDataSourceManager=_parentDataSourceManager;
@property(retain, nonatomic, getter=_plugInDiscoveryToken, setter=_setPlugInDiscoveryToken:) id plugInDiscoveryToken; // @synthesize plugInDiscoveryToken=_plugInDiscoveryToken;
// - (void).cxx_destruct;
- (void)_endContinuousPlugInDiscovery;
- (void)_beginContinuousPlugInDiscovery;
- (void)_updatePublishedWidgetExtensions;
- (void)_updatePublishedWidgetExtensions:(id)arg1;
- (void)_revokeExtensionWithIdentifier:(id)arg1;
- (void)_updateDataSourceWithExtension:(id)arg1;
- (BOOL)_shouldPublishWidgetExtension:(id)arg1;
- (void)widgetVisibilityDidChange;
- (void)_stop:(id /* CDUnknownBlockType */)arg1;
- (void)_start:(id /* CDUnknownBlockType */)arg1;
@property(readonly, nonatomic) NSArray *dataSources;
- (id)init;

@end
