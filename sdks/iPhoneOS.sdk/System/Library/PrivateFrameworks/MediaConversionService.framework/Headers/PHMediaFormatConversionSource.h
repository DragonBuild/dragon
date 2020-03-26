//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <MediaConversionService/PHMediaFormatConversionContent.h>

@class NSString;

@interface PHMediaFormatConversionSource : PHMediaFormatConversionContent
{
    BOOL _preflighted;
    BOOL _containsHEVCVideo;
    BOOL _containsHEIFImage;
    BOOL _didCheckForLivePhotoPairingIdentifier;
    NSString *_renderOriginatingSignature;
    NSString *_livePhotoPairingIdentifier;
    long long _locationMetadataStatus;
    id _hevcTrackFormatDescription;
    CGSize _imageDimensions;
}

+ (Class)requestClass;
+ (id)sourceForFileURL:(id)arg1;
+ (id)imageSourceForFileURL:(id)arg1 dimensions:(CGSize)arg2;
+ (id)imageSourceForFileURL:(id)arg1;
+ (id)videoSourceForFileURL:(id)arg1;
+ (id)sourceForFileURL:(id)arg1 mediaType:(long long)arg2 imageDimensions:(CGSize)arg3;
@property(retain) id hevcTrackFormatDescription; // @synthesize hevcTrackFormatDescription=_hevcTrackFormatDescription;
@property long long locationMetadataStatus; // @synthesize locationMetadataStatus=_locationMetadataStatus;
@property BOOL didCheckForLivePhotoPairingIdentifier; // @synthesize didCheckForLivePhotoPairingIdentifier=_didCheckForLivePhotoPairingIdentifier;
@property(retain, nonatomic) NSString *livePhotoPairingIdentifier; // @synthesize livePhotoPairingIdentifier=_livePhotoPairingIdentifier;
@property BOOL containsHEIFImage; // @synthesize containsHEIFImage=_containsHEIFImage;
@property BOOL containsHEVCVideo; // @synthesize containsHEVCVideo=_containsHEVCVideo;
@property BOOL preflighted; // @synthesize preflighted=_preflighted;
@property CGSize imageDimensions; // @synthesize imageDimensions=_imageDimensions;
@property(copy) NSString *renderOriginatingSignature; // @synthesize renderOriginatingSignature=_renderOriginatingSignature;
// - (void).cxx_destruct;
- (void)markLocationMetadataAsCheckedWithStatus:(long long)arg1;
- (long long)videoSourceLocationMetadataStatus;
- (long long)imageSourceLocationMetadataStatus;
- (void)checkForLocationData;
- (void)checkForLivePhotoPairingIdentifier;
- (void)markLivePhotoPairingIdentifierAsCheckedWithValue:(id)arg1;
- (BOOL)preflightWithError:(id )arg1;
- (void)checkForHEIFImage;
- (void)checkForHEVCVideo;
- (BOOL)determineMediaTypeFromPathExtensionWithError:(id )arg1;

@end
