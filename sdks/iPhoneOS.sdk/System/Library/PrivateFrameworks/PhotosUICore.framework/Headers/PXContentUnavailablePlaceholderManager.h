//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <PhotosUICore/PXPhotoLibraryUIChangeObserver-Protocol.h>
#import <PhotosUICore/PXSectionedDataSourceManagerObserver-Protocol.h>

@class NSString, PHFetchResult, PXGadgetDataSourceManager;
@protocol PXContentUnavailablePlaceholderManagerDelegate;

@interface PXContentUnavailablePlaceholderManager : NSObject <PXSectionedDataSourceManagerObserver, PXPhotoLibraryUIChangeObserver>
{
    struct {
        BOOL didChange;
    } _delegateRespondsTo;
    BOOL _dataSourceEmpty;
    BOOL _libraryEmpty;
    id <PXContentUnavailablePlaceholderManagerDelegate> _delegate;
    NSString *_customTitle;
    NSString *_customMessage;
    PXGadgetDataSourceManager *_gadgetDataSourceManager;
    PHFetchResult *_singleAssetFetchResult;
}

@property(nonatomic, getter=isLibraryEmpty) BOOL libraryEmpty; // @synthesize libraryEmpty=_libraryEmpty;
@property(nonatomic, getter=isDataSourceEmpty) BOOL dataSourceEmpty; // @synthesize dataSourceEmpty=_dataSourceEmpty;
@property(retain, nonatomic) PHFetchResult *singleAssetFetchResult; // @synthesize singleAssetFetchResult=_singleAssetFetchResult;
@property(retain, nonatomic) PXGadgetDataSourceManager *gadgetDataSourceManager; // @synthesize gadgetDataSourceManager=_gadgetDataSourceManager;
@property(readonly, nonatomic) NSString *customMessage; // @synthesize customMessage=_customMessage;
@property(readonly, nonatomic) NSString *customTitle; // @synthesize customTitle=_customTitle;
@property(nonatomic) __weak id <PXContentUnavailablePlaceholderManagerDelegate> delegate; // @synthesize delegate=_delegate;
// - (void).cxx_destruct;
- (void)photoLibraryDidChangeOnMainQueue:(id)arg1;
- (void)observable:(id)arg1 didChange:(NSUInteger)arg2 context:(void )arg3;
- (void)_invalidate;
- (void)_gadgetDataSourceDidChange;
- (void)performPlaceholderButtonAction;
@property(readonly, nonatomic) NSString *placeholderButtonTitle;
@property(readonly, nonatomic) NSString *placeholderMessage;
@property(readonly, nonatomic) NSString *placeholderTitle;
@property(readonly, nonatomic) BOOL wantsPlaceholder;
- (id)initWithGadgetDataSourceManager:(id)arg1 customTitle:(id)arg2 customMessage:(id)arg3;
- (id)init;

@end
