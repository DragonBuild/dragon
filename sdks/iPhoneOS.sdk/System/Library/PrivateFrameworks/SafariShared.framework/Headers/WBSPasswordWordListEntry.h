//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class NSString;

@interface WBSPasswordWordListEntry : NSObject
{
    BOOL _sensitive;
    NSString *_word;
    NSString *_wordListIdentifier;
    NSUInteger _guessesRequired;
}

@property(readonly, nonatomic) NSUInteger guessesRequired; // @synthesize guessesRequired=_guessesRequired;
@property(readonly, copy, nonatomic) NSString *wordListIdentifier; // @synthesize wordListIdentifier=_wordListIdentifier;
@property(readonly, nonatomic, getter=isSensitive) BOOL sensitive; // @synthesize sensitive=_sensitive;
@property(readonly, copy, nonatomic) NSString *word; // @synthesize word=_word;
// - (void).cxx_destruct;
- (id)description;
- (id)initWithWord:(id)arg1 isSensitive:(BOOL)arg2 wordListIdentifier:(id)arg3 guessesRequired:(NSUInteger)arg4;

@end
