//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <DataDetectorsCore/DataDetectorsSourceAccessProtocol-Protocol.h>

@interface DataDetectorsSourceAccess : NSObject <DataDetectorsSourceAccessProtocol>
{
    CDStruct_4c969caf _auditToken;
    int _clientpid;
    unsigned int _clientuid;
    BOOL _privacyUserReadEntitled;
    unsigned char _privacyUserReadEntitlementChecked;
    BOOL _privacyUserWriteEntitled;
    unsigned char _privacyUserWriteEntitlementChecked;
    BOOL _privacySystemWriteEntitled;
    unsigned char _privacySystemWriteEntitlementChecked;
}

@property unsigned int userIdentifier; // @synthesize userIdentifier=_clientuid;
@property int processIdentifier; // @synthesize processIdentifier=_clientpid;
@property CDStruct_4c969caf auditToken; // @synthesize auditToken=_auditToken;
- (BOOL)pushSourcesContent:(id)arg1 forSource:(int)arg2 signature:(id)arg3;
- (BOOL)clientCanWriteSource:(int)arg1;
- (id)fileHandleForSourceRead:(int)arg1 resourceType:(NSUInteger)arg2;
- (BOOL)privacySystemWriteEntitled;
- (BOOL)privacyUserWriteEntitled;
- (BOOL)privacyUserReadEntitled;
- (void)writeSourceFromJSONFile:(id)arg1 source:(id)arg2 withReply:(id /* CDUnknownBlockType */)arg3;
- (void)writeSourceFromRawData:(id)arg1 source:(id)arg2 signature:(id)arg3 withReply:(id /* CDUnknownBlockType */)arg4;
- (void)filesForSourceRead:(id)arg1 resourceType:(NSUInteger)arg2 withReply:(id /* CDUnknownBlockType */)arg3;
- (void)fileForSourceRead:(id)arg1 resourceType:(NSUInteger)arg2 withReply:(id /* CDUnknownBlockType */)arg3;

@end
