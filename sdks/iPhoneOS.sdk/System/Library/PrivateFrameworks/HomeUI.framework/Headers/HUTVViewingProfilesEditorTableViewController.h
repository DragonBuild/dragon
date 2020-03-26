//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <HomeUI/HUItemTableViewController.h>

#import <HomeUI/HUItemTableModuleControllerHosting-Protocol.h>

@class HUTVViewingProfilesDevicesModuleController;

@interface HUTVViewingProfilesEditorTableViewController : HUItemTableViewController <HUItemTableModuleControllerHosting>
{
    BOOL _hideHeadersAndFooters;
    HUTVViewingProfilesDevicesModuleController *_tvpDevicesModuleController;
}

@property(readonly, nonatomic) HUTVViewingProfilesDevicesModuleController *tvpDevicesModuleController; // @synthesize tvpDevicesModuleController=_tvpDevicesModuleController;
@property(nonatomic) BOOL hideHeadersAndFooters; // @synthesize hideHeadersAndFooters=_hideHeadersAndFooters;
// - (void).cxx_destruct;
- (id)moduleController:(id)arg1 textFieldForVisibleItem:(id)arg2;
- (id)moduleController:(id)arg1 dismissViewControllerForRequest:(id)arg2;
- (id)moduleController:(id)arg1 presentViewControllerForRequest:(id)arg2;
- (BOOL)shouldHideFooterBelowSection:(long long)arg1;
- (BOOL)shouldHideHeaderAboveSection:(long long)arg1;
- (id)itemModuleControllers;
- (BOOL)automaticallyUpdatesViewControllerTitle;
- (id)initWithUserItem:(id)arg1;

@end
