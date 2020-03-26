//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <CoreUI/CUIThemeRendition.h>

@class CUIRenditionMetrics, CUIRenditionSliceInformation, NSMutableArray, _CSIRenditionBlockData;

__attribute__((visibility("hidden")))
@interface _CUIThemePixelRendition : CUIThemeRendition
{
    unsigned int _nimages;
    CGImage _image[16];
    CGImage _unslicedImage;
    CUIRenditionMetrics *_renditionMetrics;
    CUIRenditionSliceInformation *_sliceInformation;
    _CSIRenditionBlockData *_cachedBlockDataBGRX;
    _CSIRenditionBlockData *_cachedBlockDataRGBX;
    _CSIRenditionBlockData *_cachedBlockDataGray;
    NSUInteger _sourceRowbytes;
    NSMutableArray *_layers;
    CGSize _unslicedSize;
}

- (BOOL)edgesOnly;
- (BOOL)isScaled;
- (BOOL)isTiled;
- (id)sliceInformation;
- (id)metrics;
- (id)layerReferences;
- (id)maskForSliceIndex:(long long)arg1;
- (id)imageForSliceIndex:(long long)arg1;
- (CGImage )unslicedImage;
- (void)dealloc;
- (NSUInteger)sourceRowbytes;
- (void)setSharedBlockData:(id)arg1;
- (id)copySharedBlockDataWithPixelFormat:(int)arg1;
- (CGSize)unslicedSize;
- (int)pixelFormat;
- (id)_initWithCSIHeader:(const struct _csiheader )arg1;
- (CGImage )newImageFromCSIDataSlice:(struct _slice)arg1 ofBitmap:(struct _csibitmap )arg2 usingColorspace:(CGColorSpace )arg3;
- (id)initWithCSIData:(id)arg1 forKey:(const struct _renditionkeytoken )arg2 artworkStatus:(long long)arg3;

@end
