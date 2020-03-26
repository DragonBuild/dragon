//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <SafariShared/WBSHistoryStoreDelegate-Protocol.h>

@class NSArray, NSCountedSet, NSData, NSMutableDictionary, WBSHistoryTagMap;
@protocol OS_dispatch_queue, WBSHistoryStore;

@interface WBSHistory : NSObject <WBSHistoryStoreDelegate>
{
    NSObject<OS_dispatch_queue> *_entriesByURLStringAccessQueue;
    NSMutableDictionary *_entriesByURLString;
    NSObject<OS_dispatch_queue> *_hostnameToHistoryItemCountAccessQueue;
    NSCountedSet *_hostnameToHistoryItemCount;
    NSCountedSet *_stringsForUserTypedDomainExpansion;
    double _historyAgeLimit;
    BOOL _hasStartedLoadingHistory;
    NSObject<OS_dispatch_queue> *_waitUntilHistoryHasLoadedQueue;
    id <WBSHistoryStore> _historyStore;
    WBSHistoryTagMap *_historyTagMap;
}

+ (void)clearExistingSharedHistory;
+ (id)historyDatabaseWriteAheadLogURL;
+ (id)historyDatabaseURL;
+ (id)historyPropertyListURL;
+ (id)existingSharedHistory;
@property(readonly, nonatomic) WBSHistoryTagMap *historyTagMap; // @synthesize historyTagMap=_historyTagMap;
@property(nonatomic) double historyAgeLimit; // @synthesize historyAgeLimit=_historyAgeLimit;
// - (void).cxx_destruct;
- (Class)_historyItemClass;
- (void)_addVisitedLinksForItemsIfNeeded:(id)arg1;
- (void)_removeAllVisitedLinks;
- (id)_createHistoryStore;
- (void)_unload;
- (void)historyStore:(id)arg1 didRemoveItems:(id)arg2;
- (void)historyStore:(id)arg1 didRemoveVisits:(id)arg2;
- (void)historyStore:(id)arg1 didAddVisits:(id)arg2;
- (void)historyStoreDidFailDatabaseIntegrityCheck:(id)arg1;
- (BOOL)historyStoreShouldCheckDatabaseIntegrity:(id)arg1;
- (void)_dispatchDidRemoveHostnames:(id)arg1;
- (void)_dispatchHistoryVisitAdded:(id)arg1;
- (void)_dispatchHistoryCleared:(id)arg1;
- (void)_dispatchHistoryItemsRemovedDuringLoading:(id)arg1;
- (void)_dispatchHistoryItemsRemoved:(id)arg1;
- (void)_dispatchHistoryItemDidChange:(id)arg1 byUserInitiatedAction:(BOOL)arg2;
- (void)_dispatchHistoryItemWillChange:(id)arg1;
- (void)_dispatchHistoryItemsAdded:(id)arg1 byUserInitiatedAction:(BOOL)arg2;
- (void)_dispatchHistoryItemsLoaded:(id)arg1;
- (void)_dispatchHistoryLoaded;
- (void)_sendNotification:(id)arg1 withItems:(id)arg2;
- (void)historyStore:(id)arg1 didPrepareToDeleteWithDeletionPlan:(id)arg2;
- (void)historyLoaderDidFinishLoading:(id)arg1;
- (void)historyLoader:(id)arg1 didLoadItems:(id)arg2 discardedItems:(id)arg3 stringsForUserTypeDomainExpansion:(id)arg4;
- (void)savePendingChangesBeforeTerminationWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)performBlockAfterHistoryHasLoaded:(id /* CDUnknownBlockType */)arg1;
- (void)waitUntilHistoryHasLoaded;
- (void)_waitUntilHistoryHasLoadedMainThread;
- (void)_startLoading;
- (void)_loadHistory;
- (void)_loadHistoryAsynchronouslyIfNeeded;
- (void)closeWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)close;
- (void)performMaintenance:(id /* CDUnknownBlockType */)arg1;
- (void)performMaintenance;
- (void)_clearHostnameCount;
- (id)_updateHostnameCountWithDeletedHistoryItems:(id)arg1;
- (void)_updateHostnameCountWithAddedHistoryItems:(id)arg1;
- (void)vacuumHistoryWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)clearHistoryWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)clearHistory;
- (void)clearHistoryVisitsAddedAfterDate:(id)arg1 beforeDate:(id)arg2 completionHandler:(id /* CDUnknownBlockType */)arg3;
- (void)clearHistoryVisitsAddedAfterDate:(id)arg1 beforeDate:(id)arg2;
- (void)setTitle:(id)arg1 ofTag:(id)arg2 completionHandler:(id /* CDUnknownBlockType */)arg3;
- (void)addTagWithIdentifier:(id)arg1 title:(id)arg2 toItemAtURL:(id)arg3 level:(long long)arg4 completionHandler:(id /* CDUnknownBlockType */)arg5;
- (void)fetchTopicsFromStartDate:(id)arg1 toEndDate:(id)arg2 limit:(NSUInteger)arg3 minimumItemCount:(NSUInteger)arg4 sortOrder:(long long)arg5 completionHandler:(id /* CDUnknownBlockType */)arg6;
- (void)fetchTopicsFromStartDate:(id)arg1 toEndDate:(id)arg2 completionHandler:(id /* CDUnknownBlockType */)arg3;
- (void)removeAttributes:(NSUInteger)arg1 fromVisit:(id)arg2;
- (void)addAttributes:(NSUInteger)arg1 toVisit:(id)arg2;
- (void)_setAttributes:(NSUInteger)arg1 forVisit:(id)arg2;
- (void)updateTitle:(id)arg1 forVisit:(id)arg2;
- (BOOL)canRecordRedirectFromVisit:(id)arg1 to:(id)arg2;
- (void)checkIfLocalVisitExistsInAnyOfItems:(id)arg1 withCompletion:(id /* CDUnknownBlockType */)arg2;
- (void)getVisitsCreatedAfterDate:(id)arg1 beforeDate:(id)arg2 completionHandler:(id /* CDUnknownBlockType */)arg3;
- (id)itemRedirectedFrom:(id)arg1 to:(id)arg2 origin:(long long)arg3 date:(id)arg4;
- (id)itemVisitedAtURLString:(id)arg1 title:(id)arg2 timeOfVisit:(double)arg3 wasHTTPNonGet:(BOOL)arg4 wasFailure:(BOOL)arg5 increaseVisitCount:(BOOL)arg6 origin:(long long)arg7 attributes:(NSUInteger)arg8;
- (id)itemVisitedAtURLString:(id)arg1 title:(id)arg2 timeOfVisit:(double)arg3 wasHTTPNonGet:(BOOL)arg4 wasFailure:(BOOL)arg5 increaseVisitCount:(BOOL)arg6 origin:(long long)arg7;
- (id)itemVisitedAtURLString:(id)arg1 title:(id)arg2 wasHTTPNonGet:(BOOL)arg3 wasFailure:(BOOL)arg4 increaseVisitCount:(BOOL)arg5;
- (void)resetCloudHistoryDataWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)setLastSeenDate:(id)arg1 forCloudClientVersion:(NSUInteger)arg2;
- (id)lastSeenDateForCloudClientVersion:(NSUInteger)arg1;
- (void)pruneTombstonesWithEndDatePriorToDate:(id)arg1;
- (void)replayAndAddTombstones:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)getAllTombstonesWithCompletion:(id /* CDUnknownBlockType */)arg1;
@property(nonatomic) BOOL syncsWithManateeContainer;
@property(nonatomic) BOOL pushNotificationsAreInitialized;
@property(nonatomic) NSUInteger cachedNumberOfDevicesInSyncCircle;
@property(copy, nonatomic) NSData *longLivedSaveOperationData;
@property(copy, nonatomic) NSData *syncCircleSizeRetrievalThrottlerData;
@property(copy, nonatomic) NSData *fetchThrottlerData;
@property(copy, nonatomic) NSData *pushThrottlerData;
- (void)setServerChangeTokenData:(id)arg1;
- (void)getServerChangeTokenDataWithCompletion:(id /* CDUnknownBlockType */)arg1;
- (void)updateHistoryAfterSuccessfulPersistedLongLivedSaveOperationWithGeneration:(long long)arg1 completion:(id /* CDUnknownBlockType */)arg2;
- (void)visitIdentifiersMatchingExistingVisits:(id)arg1 populateAssociatedVisits:(BOOL)arg2 completion:(id /* CDUnknownBlockType */)arg3;
- (void)getVisitsAndTombstonesNeedingSyncWithVisitSyncWindow:(double)arg1 completion:(id /* CDUnknownBlockType */)arg2;
- (void)enumerateItemsAsynchronouslyUsingBlock:(id /* CDUnknownBlockType */)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)enumerateItemsUsingBlock:(id /* CDUnknownBlockType */)arg1;
@property(readonly, nonatomic) NSUInteger numberOfHistoryItemsOnHistoryQueue;
@property(readonly, nonatomic) NSUInteger numberOfHistoryItems;
@property(readonly, nonatomic) BOOL hasAnyHistoryItems;
@property(readonly) NSArray *allItems;
- (void)_removeItemFromStringsForUserTypedDomainExpansion:(id)arg1;
- (void)_addItemToStringsForUserTypedDomainExpansion:(id)arg1;
- (BOOL)_isStringForUserTypedDomainExpansionInHistory:(id)arg1;
- (id)_removeItemForURLString:(id)arg1;
- (void)_addItem:(id)arg1 addToStringsForUserTypedDomainExpansions:(BOOL)arg2;
- (void)addAutocompleteTrigger:(id)arg1 forURLString:(id)arg2;
- (id)itemForURL:(id)arg1;
- (void)_removeItemsInResponseToUserAction:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)_removeHistoryItemsInResponseToUserAction:(id)arg1;
- (void)removeItemsInResponseToUserAction:(id)arg1;
- (id)itemForURLString:(id)arg1 createIfNeeded:(BOOL)arg2;
- (id)itemForURLString:(id)arg1;
- (id)init;

@end
