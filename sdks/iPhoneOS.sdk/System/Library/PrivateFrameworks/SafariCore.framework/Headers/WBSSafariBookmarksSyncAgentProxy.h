//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <SafariCore/WBSSafariBookmarksSyncAgentProtocol-Protocol.h>

@class NSXPCConnection;

@interface WBSSafariBookmarksSyncAgentProxy : NSObject <WBSSafariBookmarksSyncAgentProtocol>
{
    NSXPCConnection *__connection;
}

+ (id)sharedProxy;
@property(retain) NSXPCConnection *_connection; // @synthesize _connection=__connection;
// - (void).cxx_destruct;
- (void)migrateToCloudKitWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)generateDAVServerIDsForExistingBookmarksWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)clearLocalDataIncludingMigrationState:(BOOL)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)resetToDAVDatabaseWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)getCloudTabDevicesWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)fetchSyncedCloudTabDevicesAndCloseRequestsWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)deleteCloudTabCloseRequestsWithUUIDStrings:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)deleteDevicesWithUUIDStrings:(id)arg1 completionHandler:(id /* CDUnknownBlockType */)arg2;
- (void)saveCloudTabCloseRequestWithDictionaryRepresentation:(id)arg1 closeRequestUUIDString:(id)arg2 completionHandler:(id /* CDUnknownBlockType */)arg3;
- (void)saveTabsForCurrentDeviceWithDictionaryRepresentation:(id)arg1 deviceUUIDString:(id)arg2 completionHandler:(id /* CDUnknownBlockType */)arg3;
- (void)collectDiagnosticsDataWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)beginMigrationFromDAV;
- (void)observeRemoteMigrationStateForSecondaryMigration;
- (void)fetchRemoteMigrationStateWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)userDidUpdateBookmarkDatabase;
- (void)userAccountDidChange:(long long)arg1;
- (void)fetchUserIdentityWithCompletionHandler:(id /* CDUnknownBlockType */)arg1;
- (void)setUsesOpportunisticPushTopic:(BOOL)arg1;
- (void)registerForPushNotificationsIfNeeded;
- (void)dealloc;
- (id)init;

@end
