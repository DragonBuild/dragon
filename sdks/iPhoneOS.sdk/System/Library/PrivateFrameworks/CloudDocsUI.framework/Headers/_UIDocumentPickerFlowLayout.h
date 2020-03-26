//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UICollectionViewFlowLayout.h>

#import <CloudDocsUI/_UICollectionViewLayoutCellStyle-Protocol.h>

__attribute__((visibility("hidden")))
@interface _UIDocumentPickerFlowLayout : UICollectionViewFlowLayout <_UICollectionViewLayoutCellStyle>
{
    long long cellStyle;
    double _contentSizeAdjustment;
}

@property(nonatomic) double contentSizeAdjustment; // @synthesize contentSizeAdjustment=_contentSizeAdjustment;
@property(nonatomic) long long cellStyle; // @synthesize cellStyle;
- (BOOL)shouldInvalidateLayoutForBoundsChange:(CGRect)arg1;
- (BOOL)canBeEdited;
- (CGSize)collectionViewContentSize;

@end
