//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <VideosUI/VUIListCollectionViewCell.h>

@class IKViewElement, VUIFavoriteView;

__attribute__((visibility("hidden")))
@interface VUIFavoriteCollectionViewCell : VUIListCollectionViewCell
{
    VUIFavoriteView *_favoriteView;
    IKViewElement *_viewElement;
}

+ (id)configureWithElement:(id)arg1 existingView:(id)arg2;
@property(retain, nonatomic) IKViewElement *viewElement; // @synthesize viewElement=_viewElement;
@property(retain, nonatomic) VUIFavoriteView *favoriteView; // @synthesize favoriteView=_favoriteView;
// - (void).cxx_destruct;
- (CGSize)sizeThatFits:(CGSize)arg1;
- (void)setHighlighted:(BOOL)arg1;
- (void)layoutSubviews;
- (void)prepareForReuse;
- (id)initWithFrame:(CGRect)arg1;

@end
