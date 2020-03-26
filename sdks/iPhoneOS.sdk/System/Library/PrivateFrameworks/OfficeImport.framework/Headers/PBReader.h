//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <OfficeImport/OCBReader.h>

__attribute__((visibility("hidden")))
@interface PBReader : OCBReader
{
    struct PptObjectFactory mPptObjectFactory;
    const void mBuffer;
}

- (struct OCCBinaryStreamer )allocBinaryStreamerWithCryptoKey:(struct OCCCryptoKey )arg1 baseOutputFilenameInUTF8:(const char )arg2;
- (struct OCCEncryptionInfoReader )encryptionInfoReader;
@property(readonly, nonatomic) struct PptBinaryReader pptReader;
- (id)read;
- (BOOL)start;
- (void)dealloc;
- (id)initWithCancelDelegate:(id)arg1;

@end
