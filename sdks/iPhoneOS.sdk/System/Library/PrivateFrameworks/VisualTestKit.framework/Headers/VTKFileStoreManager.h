//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <VisualTestKit/VTKStoreManager-Protocol.h>

@class NSString, NSURL;

__attribute__((visibility("hidden")))
@interface VTKFileStoreManager : NSObject <VTKStoreManager>
{
    NSString *_itemsDirectory;
    NSURL *_saveItemsRootURL;
}

@property(readonly, nonatomic) NSURL *saveItemsRootURL; // @synthesize saveItemsRootURL=_saveItemsRootURL;
@property(copy, nonatomic) NSString *itemsDirectory; // @synthesize itemsDirectory=_itemsDirectory;
// - (void).cxx_destruct;
- (id)saveItems:(id)arg1 withID:(id)arg2 testCase:(id)arg3;
- (id)init;

@end
