//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//


@class REElement, RERelevanceEngine, RESectionPath;

@protocol RERelevanceEngineObserver <NSObject>

@optional
- (void)relevanceEngineDidFinishUpdatingRelevance:(RERelevanceEngine *)arg1;
- (void)relevanceEngineDidBeginUpdatingRelevance:(RERelevanceEngine *)arg1;
- (void)relevanceEngine:(RERelevanceEngine *)arg1 didUpdateRelevanceForElement:(REElement *)arg2;
- (BOOL)relevanceEngine:(RERelevanceEngine *)arg1 isElementAtPathVisible:(RESectionPath *)arg2;
- (void)relevanceEngine:(RERelevanceEngine *)arg1 didMoveElement:(REElement *)arg2 fromPath:(RESectionPath *)arg3 toPath:(RESectionPath *)arg4;
- (void)relevanceEngine:(RERelevanceEngine *)arg1 didInsertElement:(REElement *)arg2 atPath:(RESectionPath *)arg3;
- (void)relevanceEngine:(RERelevanceEngine *)arg1 didRemoveElement:(REElement *)arg2 atPath:(RESectionPath *)arg3;
- (void)relevanceEngine:(RERelevanceEngine *)arg1 didReloadElement:(REElement *)arg2 atPath:(RESectionPath *)arg3;
- (void)relevanceEngine:(RERelevanceEngine *)arg1 performBatchUpdateBlock:(void (^)(void))arg2 completion:(void (^)(void))arg3;
@end
