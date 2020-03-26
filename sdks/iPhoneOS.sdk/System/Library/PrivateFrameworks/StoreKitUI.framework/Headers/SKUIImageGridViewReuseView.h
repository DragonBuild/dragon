//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <StoreKitUI/SKUIViewReuseView.h>

#import <StoreKitUI/SKUIViewElementView-Protocol.h>

@class NSArray, NSMapTable, SKUIImageGridViewElement;

__attribute__((visibility("hidden")))
@interface SKUIImageGridViewReuseView : SKUIViewReuseView <SKUIViewElementView>
{
    NSMapTable *_imageViewToImageResourceCacheKey;
    NSMapTable *_viewElementViews;
    SKUIImageGridViewElement *_imageGridViewElement;
    NSArray *_imageViews;
}

+ (CGSize)sizeThatFitsWidth:(double)arg1 viewElement:(id)arg2 context:(id)arg3;
+ (void)requestLayoutForViewElement:(id)arg1 width:(double)arg2 context:(id)arg3;
+ (CGSize)preferredSizeForViewElement:(id)arg1 context:(id)arg2;
+ (BOOL)prefetchResourcesForViewElement:(id)arg1 reason:(long long)arg2 context:(id)arg3;
@property(retain, nonatomic) NSArray *imageViews; // @synthesize imageViews=_imageViews;
// - (void).cxx_destruct;
- (id)viewForElementIdentifier:(id)arg1;
- (BOOL)updateWithItemState:(id)arg1 context:(id)arg2 animated:(BOOL)arg3;
- (BOOL)setImage:(id)arg1 forArtworkRequest:(id)arg2 context:(id)arg3;
- (void)setContentInset:(UIEdgeInsets)arg1;
- (void)reloadWithViewElement:(id)arg1 width:(double)arg2 context:(id)arg3;
- (id)init;

@end
