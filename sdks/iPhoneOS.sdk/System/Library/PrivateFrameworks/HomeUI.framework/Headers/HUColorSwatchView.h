//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UIView.h>

@class CAShapeLayer, NSString, UIColor, UILabel;

@interface HUColorSwatchView : UIView
{
    BOOL _labelHidden;
    NSUInteger _selectionState;
    NSString *_text;
    CAShapeLayer *_circleLayer;
    CAShapeLayer *_selectedCircleLayer;
    CAShapeLayer *_selectedCircleInnerLayer;
    CAShapeLayer *_selectedCircleOuterLayer;
    UILabel *_label;
}

+ (Class)layerClass;
@property(retain, nonatomic) UILabel *label; // @synthesize label=_label;
@property(retain, nonatomic) CAShapeLayer *selectedCircleOuterLayer; // @synthesize selectedCircleOuterLayer=_selectedCircleOuterLayer;
@property(retain, nonatomic) CAShapeLayer *selectedCircleInnerLayer; // @synthesize selectedCircleInnerLayer=_selectedCircleInnerLayer;
@property(retain, nonatomic) CAShapeLayer *selectedCircleLayer; // @synthesize selectedCircleLayer=_selectedCircleLayer;
@property(retain, nonatomic) CAShapeLayer *circleLayer; // @synthesize circleLayer=_circleLayer;
@property(retain, nonatomic) NSString *text; // @synthesize text=_text;
@property(nonatomic) BOOL labelHidden; // @synthesize labelHidden=_labelHidden;
@property(nonatomic) NSUInteger selectionState; // @synthesize selectionState=_selectionState;
// - (void).cxx_destruct;
- (BOOL)_shouldAnimatePropertyWithKey:(id)arg1;
- (void)layoutSubviews;
- (void)traitCollectionDidChange:(id)arg1;
- (void)_updateTextColor;
- (void)_updateLayout;
@property(retain, nonatomic) UIColor *color;
- (id)initWithFrame:(CGRect)arg1 text:(id)arg2;
- (id)initWithFrame:(CGRect)arg1;

@end
