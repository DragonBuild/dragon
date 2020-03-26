//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <HomeUI/HUItemTableModuleController.h>

#import <HomeUI/MCProfileViewControllerDelegate-Protocol.h>

@protocol HUAccessorySettingsProfileModuleControllerDelegate;

@interface HUAccessorySettingsProfileModuleController : HUItemTableModuleController <MCProfileViewControllerDelegate>
{
    id <HUAccessorySettingsProfileModuleControllerDelegate> _delegate;
}

@property(nonatomic) __weak id <HUAccessorySettingsProfileModuleControllerDelegate> delegate; // @synthesize delegate=_delegate;
// - (void).cxx_destruct;
- (void)profileViewControllerDidSelectRemoveProfile:(id)arg1;
- (NSUInteger)didSelectItem:(id)arg1;
- (void)setupCell:(id)arg1 forItem:(id)arg2;
- (Class)cellClassForItem:(id)arg1;
- (id)initWithModule:(id)arg1;

@end
