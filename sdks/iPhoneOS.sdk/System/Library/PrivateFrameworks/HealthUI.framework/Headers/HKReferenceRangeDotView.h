//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UIView.h>

@class UIColor, _HKReferenceRangeDotViewDot;

@interface HKReferenceRangeDotView : UIView
{
    _HKReferenceRangeDotViewDot *_dotView;
}

@property(nonatomic) __weak _HKReferenceRangeDotViewDot *dotView; // @synthesize dotView=_dotView;
// - (void).cxx_destruct;
@property(retain, nonatomic) UIColor *dotColor;
- (CGRect)desiredDotViewFrame;
- (void)setFrame:(CGRect)arg1;
- (id)initWithFrame:(CGRect)arg1;

@end
