//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <EmailCore/ECTransferActionReplayer.h>

#import <EmailCore/ECIMAPLocalActionReplayer-Protocol.h>
#import <EmailCore/ECTransferActionReplayerSubclassMethods-Protocol.h>

@protocol ECIMAPLocalActionReplayerDelegate, ECIMAPServerInterface;

@interface ECTransferActionIMAPReplayer : ECTransferActionReplayer <ECTransferActionReplayerSubclassMethods, ECIMAPLocalActionReplayer>
{
    id <ECIMAPServerInterface> serverInterface;
    id <ECIMAPLocalActionReplayerDelegate> delegate;
}

@property(nonatomic) __weak id <ECIMAPLocalActionReplayerDelegate> delegate; // @synthesize delegate;
@property(retain, nonatomic) id <ECIMAPServerInterface> serverInterface; // @synthesize serverInterface;
// - (void).cxx_destruct;
- (id)appendItem:(id)arg1 mailboxURL:(id)arg2;
- (BOOL)isRecoverableError:(id)arg1;
- (BOOL)downloadFailed;
- (id)fetchBodyDataForRemoteID:(id)arg1 mailboxURL:(id)arg2;
- (BOOL)deleteSourceMessagesFromTransferItems:(id)arg1;
- (id)_transferItems:(id)arg1 destinationMailboxURL:(id)arg2 isMove:(BOOL)arg3;
- (id)copyItems:(id)arg1 destinationMailboxURL:(id)arg2;
- (id)moveItems:(id)arg1 destinationMailboxURL:(id)arg2;

@end
