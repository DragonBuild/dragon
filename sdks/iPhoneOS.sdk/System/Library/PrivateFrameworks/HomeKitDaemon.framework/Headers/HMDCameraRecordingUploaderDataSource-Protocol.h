//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//


@class CKStreamingAssetAppendContext, HMDCameraRecordingUploadOperationEvent, HMFTimer, NSData, NSURL;

@protocol HMDCameraRecordingUploaderDataSource <NSObject>
@property(readonly, copy) NSURL *storeDirectoryURL;
- (void)submitOperationEvent:(HMDCameraRecordingUploadOperationEvent *)arg1;
- (HMFTimer *)timerWithTimeInterval:(double)arg1 options:(NSUInteger)arg2;
- (void)appendData:(NSData *)arg1 toStreamingAssetAppendContext:(CKStreamingAssetAppendContext *)arg2 completion:(void (^)(CKStreamingAsset *, NSError *))arg3;
- (BOOL)removeItemAtURL:(NSURL *)arg1 error:(id )arg2;
- (BOOL)writeData:(NSData *)arg1 toFileAtURL:(NSURL *)arg2 error:(id )arg3;
- (BOOL)createDirectoryAtURL:(NSURL *)arg1 withIntermediateDirectories:(BOOL)arg2 error:(id )arg3;
@end
