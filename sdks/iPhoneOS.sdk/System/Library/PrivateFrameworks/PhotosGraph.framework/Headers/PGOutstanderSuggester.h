//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <PhotosGraph/PGAbstractSuggester.h>

#import <PhotosGraph/PGCoordinatableSuggester-Protocol.h>

@class NSArray, NSDictionary, NSEnumerator, PGSuggestionOptions;

@interface PGOutstanderSuggester : PGAbstractSuggester <PGCoordinatableSuggester>
{
    PGSuggestionOptions *_options;
    NSDictionary *_assetUUIDsByScore;
    NSArray *_sortedScores;
    long long _currentScoreIndex;
    NSEnumerator *_currentSuggestedAssetEnumerator;
}

+ (id)suggestionSubtypes;
+ (id)suggestionTypes;
// - (void).cxx_destruct;
- (id)reasonsForSuggestion:(id)arg1;
- (id)nextSuggestedAssetEnumerator;
- (id)nextSuggestedAsset;
- (NSUInteger)scoreWithAsset:(id)arg1;
- (void)computeNiceAssetsBetweenStartDate:(id)arg1 andEndDate:(id)arg2;
- (void)reset;
- (id)nextSuggestion;
- (void)startSuggestingWithOptions:(id)arg1;
- (id)suggestionsWithOptions:(id)arg1 progress:(id /* CDUnknownBlockType */)arg2;

@end
