//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UIView.h>

@class MISSING_TYPE;

@interface _TtC26DocumentManagerExecutables23DOCContainerFittingView : UIView
{
    MISSING_TYPE *containedViewController;
    MISSING_TYPE *fittingSize;
    MISSING_TYPE *preventContentOffsetUpdates;
    MISSING_TYPE *contentOffsetFromTop;
    MISSING_TYPE *observationContext;
}

// - (void).cxx_destruct;
- (id)initWithFrame:(CGRect)arg1;
- (CGSize)systemLayoutSizeFittingSize:(CGSize)arg1;
@property(nonatomic, readonly) CGSize intrinsicContentSize;
- (id)initWithCoder:(id)arg1;
- (void)layoutSubviews;
@property(nonatomic) double contentOffsetFromTop; // @synthesize contentOffsetFromTop;

@end
