//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <NanoTimeKitCompanion/NTKAVListingFaceBaseView.h>

@class NTKComplicationDisplayWrapperView, NTKFaceViewComplicationFactory, NTKInfinityController, NTKInfinityListing, UIColor, UILabel, UIView;

@interface NTKInfinityFaceView : NTKAVListingFaceBaseView
{
    unsigned int _tapToPlayGestureEnabled:1;
    unsigned int _tapPromptedVideoChange:1;
    UIView *_cornerView;
    UILabel *_reviewLabel;
    long long _previousDataMode;
    NTKFaceViewComplicationFactory *_faceViewComplicationFactory;
    NTKComplicationDisplayWrapperView *_touchWrapper;
    NTKInfinityController *_controller;
    NTKInfinityListing *_currentQueueListing;
    UIColor *_currentComplicationColor;
}

// - (void).cxx_destruct;
- (id)_swatchImageForEditOption:(id)arg1 mode:(long long)arg2 withSelectedOptions:(id)arg3;
- (void)_updateReviewLabel;
- (void)updateReviewDirection:(id)arg1;
- (void)_handleSingleTap:(id)arg1;
- (void)touchesCancelled:(id)arg1 withEvent:(id)arg2;
- (void)touchesEnded:(id)arg1 withEvent:(id)arg2;
- (void)touchesMoved:(id)arg1 withEvent:(id)arg2;
- (void)touchesBegan:(id)arg1 withEvent:(id)arg2;
- (id)_complicationDisplayWrapperForTouch:(id)arg1;
- (id)_onDeckPosterImageView;
- (id)_posterImageView;
- (id)_posterImageViewForStyle:(NSUInteger)arg1;
- (id)_currentPosterImageView;
- (BOOL)_keylineLabelShouldShowIndividualOptionNamesForCustomEditMode:(long long)arg1;
- (NSUInteger)_keylineLabelAlignmentForComplicationSlot:(id)arg1;
- (id)_keylineViewForCustomEditMode:(long long)arg1 slot:(id)arg2;
- (long long)_complicationPickerStyleForSlot:(id)arg1;
- (BOOL)_shouldFadeToTransitionView;
- (double)_timeLabelAlphaForEditMode:(long long)arg1;
- (BOOL)_fadesComplicationSlot:(id)arg1 inEditMode:(long long)arg2;
- (void)setTransitionFraction:(double)arg1 fromOption:(id)arg2 toOption:(id)arg3 customEditMode:(long long)arg4 slot:(id)arg5;
- (void)_applyDataMode;
- (void)_cleanupAfterEditing;
- (void)_prepareForEditing;
- (void)_applyOption:(id)arg1 forCustomEditMode:(long long)arg2 slot:(id)arg3;
- (id)_viewForEditOption:(id)arg1;
- (id)_editingComplicationColor;
- (void)_updateComplicationWithColor:(id)arg1 animated:(BOOL)arg2;
- (long long)_legacyLayoutOverrideforComplicationType:(NSUInteger)arg1 slot:(id)arg2;
- (void)_configureComplicationView:(id)arg1 forSlot:(id)arg2;
- (id)_newLegacyViewForComplication:(id)arg1 family:(long long)arg2 slot:(id)arg3;
- (void)_loadLayoutRules;
- (void)didAddSubview:(id)arg1;
- (double)_adjustmentForBottomTimeLayout;
- (double)_rightSideMarginForDigitalTimeHeroPosition;
- (void)_layoutForegroundContainerView;
- (BOOL)_shouldQueueKeepAlive;
- (id)videoPlayerView;
- (void)videoPlayerViewDidPauseAfterPlayingVideoToEnd:(id)arg1;
- (void)videoPlayerViewDidBeginPlaying:(id)arg1;
- (void)videoPlayerViewDidBeginPlayingQueuedVideo:(id)arg1;
- (void)handleScreenBlanked;
- (void)_handleOrdinaryScreenWake;
- (void)_handleWristRaiseScreenWake;
- (id)_nextListing;
- (void)_selectDefaultListing;
- (void)_updatePaused;
- (void)_performPreloadVideoTask;
- (BOOL)_supportsTimeScrubbing;
- (BOOL)_wantsTimeTravelStatusModule;
- (void)layoutSubviews;
- (void)_unloadSnapshotContentViews;
- (void)_loadSnapshotContentViews;
- (void)dealloc;
- (id)initWithFaceStyle:(long long)arg1 forDevice:(id)arg2 clientIdentifier:(id)arg3;

@end
