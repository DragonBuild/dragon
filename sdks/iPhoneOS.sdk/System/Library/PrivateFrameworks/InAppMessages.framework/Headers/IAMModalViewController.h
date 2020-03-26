//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UIViewController.h>

#import <InAppMessages/_UISheetPresentationControllerDelegate-Protocol.h>

@class UIView;
@protocol IAMViewControllerMetricsDelegate;

@interface IAMModalViewController : UIViewController <_UISheetPresentationControllerDelegate>
{
    BOOL _shouldPresentFullscreen;
    BOOL _shouldUsePadLayout;
    UIViewController *_contentViewController;
    id <IAMViewControllerMetricsDelegate> _metricsDelegate;
    id /* CDUnknownBlockType */ _viewControllerWillDismissBlock;
    UIView *_contentView;
}

@property(readonly) BOOL shouldUsePadLayout; // @synthesize shouldUsePadLayout=_shouldUsePadLayout;
@property(retain, nonatomic) UIView *contentView; // @synthesize contentView=_contentView;
@property(nonatomic) BOOL shouldPresentFullscreen; // @synthesize shouldPresentFullscreen=_shouldPresentFullscreen;
@property(copy, nonatomic) id /* CDUnknownBlockType */ viewControllerWillDismissBlock; // @synthesize viewControllerWillDismissBlock=_viewControllerWillDismissBlock;
@property(nonatomic) __weak id <IAMViewControllerMetricsDelegate> metricsDelegate; // @synthesize metricsDelegate=_metricsDelegate;
@property(retain, nonatomic) UIViewController *contentViewController; // @synthesize contentViewController=_contentViewController;
// - (void).cxx_destruct;
- (void)presentationControllerDidDismiss:(id)arg1;
- (id)_presentationControllerForPresentedController:(id)arg1 presentingController:(id)arg2 sourceController:(id)arg3;
- (void)dismissViewControllerAnimated:(BOOL)arg1 completion:(id /* CDUnknownBlockType */)arg2;
- (BOOL)shouldAutorotate;
- (void)viewDidLoad;
- (long long)preferredStatusBarStyle;
- (id)init;

@end
