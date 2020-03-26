//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UIViewController.h>

#import <TeaUI/TSPresenterType-Protocol.h>

@class TSTransitionContainerViewController;

@interface UIViewController (TeaBridge) <TSPresenterType>
- (BOOL)ts_setAppearanceTransitionsAreDisabled:(BOOL)arg1;
@property(readonly, nonatomic) UIViewController *ts_parentVC;
@property(nonatomic, readonly) TSTransitionContainerViewController *ts_transitionContainerViewController;
- (void)removeCommand:(id)arg1 forContextProvider:(id)arg2;
- (void)removeCommands:(id)arg1 forContextProvider:(id)arg2;
- (void)removeContextProvider:(id)arg1;
- (void)addContextProvider:(id)arg1 forCommand:(id)arg2 completion:(id /* CDUnknownBlockType */)arg3;
- (id)tabBarSplitViewFocusable;
- (id)tabBarSplitViewFousable;
@end
