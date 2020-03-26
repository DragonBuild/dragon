//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import "UILayoutGuide.h"

@class NSLayoutConstraint;

__attribute__((visibility("hidden")))
@interface _UIContentConstraintsLayoutGuide : UILayoutGuide
{
    BOOL _wantsMaximumSizeConstraintsActive;
    BOOL _wantsMinimumSizeConstraintsActive;
    NSLayoutConstraint *_leadingConstraint;
    NSLayoutConstraint *_trailingConstraint;
    NSLayoutConstraint *_topConstraint;
    NSLayoutConstraint *_bottomConstraint;
    NSLayoutConstraint *_maximumWidthConstraint;
    NSLayoutConstraint *_maximumHeightConstraint;
    NSLayoutConstraint *_minimumWidthConstraint;
    NSLayoutConstraint *_minimumHeightConstraint;
    CGSize _maximumSize;
    CGSize _minimumSize;
    UIEdgeInsets _edgeInsets;
}

@property(readonly, nonatomic) NSLayoutConstraint *minimumHeightConstraint; // @synthesize minimumHeightConstraint=_minimumHeightConstraint;
@property(readonly, nonatomic) NSLayoutConstraint *minimumWidthConstraint; // @synthesize minimumWidthConstraint=_minimumWidthConstraint;
@property(readonly, nonatomic) BOOL wantsMinimumSizeConstraintsActive; // @synthesize wantsMinimumSizeConstraintsActive=_wantsMinimumSizeConstraintsActive;
@property(readonly, nonatomic) NSLayoutConstraint *maximumHeightConstraint; // @synthesize maximumHeightConstraint=_maximumHeightConstraint;
@property(readonly, nonatomic) NSLayoutConstraint *maximumWidthConstraint; // @synthesize maximumWidthConstraint=_maximumWidthConstraint;
@property(readonly, nonatomic) BOOL wantsMaximumSizeConstraintsActive; // @synthesize wantsMaximumSizeConstraintsActive=_wantsMaximumSizeConstraintsActive;
@property(readonly, nonatomic) NSLayoutConstraint *bottomConstraint; // @synthesize bottomConstraint=_bottomConstraint;
@property(readonly, nonatomic) NSLayoutConstraint *topConstraint; // @synthesize topConstraint=_topConstraint;
@property(readonly, nonatomic) NSLayoutConstraint *trailingConstraint; // @synthesize trailingConstraint=_trailingConstraint;
@property(readonly, nonatomic) NSLayoutConstraint *leadingConstraint; // @synthesize leadingConstraint=_leadingConstraint;
@property(nonatomic) CGSize minimumSize; // @synthesize minimumSize=_minimumSize;
@property(nonatomic) CGSize maximumSize; // @synthesize maximumSize=_maximumSize;
@property(nonatomic) UIEdgeInsets edgeInsets; // @synthesize edgeInsets=_edgeInsets;
// - (void).cxx_destruct;
- (void)_clearConstraints;
- (void)_updateAllSizeConstraints;
- (void)_updateAllMarginConstraintConstants;
- (void)_setAllSizeConstraintsActive:(BOOL)arg1;
- (void)_setAllMarginConstraintsActive:(BOOL)arg1;
- (id)_allSizeConstraints;
- (id)_allMarginConstraints;
- (void)setOwningView:(id)arg1;
- (id)init;

@end
