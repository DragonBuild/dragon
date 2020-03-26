//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UITableViewCell.h>


@class NSArray, UICollectionView;
@protocol WDHealthDataTopLevelCategoryTableViewCellDelegate;

__attribute__((visibility("hidden")))
@interface WDHealthDataTopLevelCategoryTableViewCell : UITableViewCell <UICollectionViewDataSource, UICollectionViewDelegate>
{
    NSArray *_topLevelDataCategories;
    UICollectionView *_collectionView;
    double _cachedCategoryNameFittingScaleFactor;
    id <WDHealthDataTopLevelCategoryTableViewCellDelegate> _delegate;
}

+ (double)_contentItemHeight;
+ (double)_contentItemWidth;
+ (double)_collectionViewWidth;
+ (double)contentHeightWithCount:(NSUInteger)arg1;
+ (NSUInteger)collectionViewItemsPerRow;
+ (BOOL)requiresConstraintBasedLayout;
+ (id)reuseIdentifier;
@property(nonatomic) __weak id <WDHealthDataTopLevelCategoryTableViewCellDelegate> delegate; // @synthesize delegate=_delegate;
// - (void).cxx_destruct;
- (void)traitCollectionDidChange:(id)arg1;
- (void)collectionView:(id)arg1 didSelectItemAtIndexPath:(id)arg2;
- (id)collectionView:(id)arg1 cellForItemAtIndexPath:(id)arg2;
- (long long)collectionView:(id)arg1 numberOfItemsInSection:(long long)arg2;
- (double)categoryNameLabelFontSize;
- (double)_categoryNameFittingScaleFactor;
- (double)_categoryNameWidth;
- (CGSize)_contentItemSize;
- (CGRect)_collectionViewFrame;
- (void)_setupCollectionView;
- (double)contentHeight;
- (void)dealloc;
- (id)initWithCoder:(id)arg1;
- (id)initWithStyle:(long long)arg1 reuseIdentifier:(id)arg2;
- (id)initWithTopLevelDataCategories:(id)arg1;

@end
