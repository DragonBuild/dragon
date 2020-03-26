//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <LinkPresentation/LPComponentView.h>

@class LPImageViewStyle, NSArray, NSMutableArray;

__attribute__((visibility("hidden")))
@interface LPImageStackView : LPComponentView
{
    NSArray *_images;
    LPImageViewStyle *_style;
    NSMutableArray *_imageViews;
}

// - (void).cxx_destruct;
- (CGSize)sizeThatFits:(CGSize)arg1;
- (CGSize)_layoutImagesForSize:(CGSize)arg1 applyingLayout:(BOOL)arg2;
- (void)layoutComponentView;
- (void)componentViewDidMoveToWindow;
- (id)initWithImages:(id)arg1 style:(id)arg2;
- (id)init;

@end
