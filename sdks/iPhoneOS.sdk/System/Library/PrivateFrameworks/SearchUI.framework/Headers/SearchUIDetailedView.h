//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <AppSupportUI/NUIContainerStackView.h>

#import <SearchUI/NUIContainerViewDelegate-Protocol.h>
#import <SearchUI/SearchUIAccessoryViewDelegate-Protocol.h>
#import <SearchUI/TLKDetailsViewDelegate-Protocol.h>

@class NSMutableArray, SearchUIAccessoryViewController, SearchUIDetailedRowModel, SearchUILeadingViewController, TLKDetailsView, TLKStackView;
@protocol SearchUIDetailedViewDelegate, SearchUIFeedbackDelegate;

@interface SearchUIDetailedView : NUIContainerStackView <NUIContainerViewDelegate, SearchUIAccessoryViewDelegate, TLKDetailsViewDelegate>
{
    BOOL _isVerticalAlignment;
    id <SearchUIFeedbackDelegate> _feedbackDelegate;
    id <SearchUIDetailedViewDelegate> _buttonDelegate;
    SearchUIAccessoryViewController *_currentAccessoryViewController;
    SearchUILeadingViewController *_currentLeadingViewController;
    SearchUIDetailedRowModel *_rowModel;
    TLKStackView *_innerContainer;
    NSMutableArray *_leadingViewControllers;
    TLKDetailsView *_detailsView;
    NSMutableArray *_accessoryViewControllers;
}

+ (void)addViewIfNecessary:(id)arg1 toStackView:(id)arg2 removeFromStackView:(id)arg3;
@property(retain, nonatomic) NSMutableArray *accessoryViewControllers; // @synthesize accessoryViewControllers=_accessoryViewControllers;
@property(retain, nonatomic) TLKDetailsView *detailsView; // @synthesize detailsView=_detailsView;
@property(retain, nonatomic) NSMutableArray *leadingViewControllers; // @synthesize leadingViewControllers=_leadingViewControllers;
@property(retain, nonatomic) TLKStackView *innerContainer; // @synthesize innerContainer=_innerContainer;
@property(retain, nonatomic) SearchUIDetailedRowModel *rowModel; // @synthesize rowModel=_rowModel;
@property(retain, nonatomic) SearchUILeadingViewController *currentLeadingViewController; // @synthesize currentLeadingViewController=_currentLeadingViewController;
@property(retain, nonatomic) SearchUIAccessoryViewController *currentAccessoryViewController; // @synthesize currentAccessoryViewController=_currentAccessoryViewController;
@property(nonatomic) __weak id <SearchUIDetailedViewDelegate> buttonDelegate; // @synthesize buttonDelegate=_buttonDelegate;
@property(nonatomic) __weak id <SearchUIFeedbackDelegate> feedbackDelegate; // @synthesize feedbackDelegate=_feedbackDelegate;
@property(nonatomic) BOOL isVerticalAlignment; // @synthesize isVerticalAlignment=_isVerticalAlignment;
// - (void).cxx_destruct;
- (id)hitTest:(CGPoint)arg1 withEvent:(id)arg2;
- (void)footnoteButtonPressed;
- (BOOL)arrangedViewMustCenter:(id)arg1;
- (void)updateWithRowModel:(id)arg1;
- (id)initWithFeedbackDelegate:(id)arg1;

@end
