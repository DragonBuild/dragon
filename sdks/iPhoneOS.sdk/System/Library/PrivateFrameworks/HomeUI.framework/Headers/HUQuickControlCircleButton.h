//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UIButton.h>

@class UIColor, UIView;

@interface HUQuickControlCircleButton : UIButton
{
    UIColor *_selectedColor;
    UIView *_backgroundView;
    UIColor *_standardBackgroundColor;
}

@property(retain, nonatomic) UIColor *standardBackgroundColor; // @synthesize standardBackgroundColor=_standardBackgroundColor;
@property(retain, nonatomic) UIView *backgroundView; // @synthesize backgroundView=_backgroundView;
@property(retain, nonatomic) UIColor *selectedColor; // @synthesize selectedColor=_selectedColor;
// - (void).cxx_destruct;
- (void)layoutSubviews;
- (void)_controlStateChanged;
- (void)_adjustTitleColor;
- (void)setHighlighted:(BOOL)arg1;
- (void)setEnabled:(BOOL)arg1;
@property(nonatomic) double fontSize;
- (id)initWithFrame:(CGRect)arg1;

@end
