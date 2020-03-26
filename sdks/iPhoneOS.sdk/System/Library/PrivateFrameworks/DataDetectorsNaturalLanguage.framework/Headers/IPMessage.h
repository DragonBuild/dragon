//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@class IPPerson, NSArray, NSDate, NSMutableArray, NSMutableDictionary, NSString;

@interface IPMessage : NSObject
{
    NSMutableArray *_messageUnits;
    NSMutableDictionary *_keywordsDictionary;
    NSString *_lowercaseSubject;
    BOOL _isReply;
    BOOL _isSent;
    BOOL _isGroupConversation;
    BOOL _isSenderSignificant;
    NSString *_identifier;
    NSString *_threadIdentifier;
    NSString *_subject;
    IPPerson *_sender;
    NSArray *_recipients;
    NSDate *_dateSent;
    NSString *_type;
    NSString *_htmlContent;
    NSUInteger _messageUnitsTextLength;
}

@property(readonly) NSUInteger messageUnitsTextLength; // @synthesize messageUnitsTextLength=_messageUnitsTextLength;
@property(retain) NSString *htmlContent; // @synthesize htmlContent=_htmlContent;
@property BOOL isSenderSignificant; // @synthesize isSenderSignificant=_isSenderSignificant;
@property BOOL isGroupConversation; // @synthesize isGroupConversation=_isGroupConversation;
@property BOOL isSent; // @synthesize isSent=_isSent;
@property BOOL isReply; // @synthesize isReply=_isReply;
@property(retain) NSString *type; // @synthesize type=_type;
@property(retain) NSDate *dateSent; // @synthesize dateSent=_dateSent;
@property(retain) NSArray *recipients; // @synthesize recipients=_recipients;
@property(retain) IPPerson *sender; // @synthesize sender=_sender;
@property(retain) NSString *subject; // @synthesize subject=_subject;
@property(retain) NSString *threadIdentifier; // @synthesize threadIdentifier=_threadIdentifier;
@property(retain) NSString *identifier; // @synthesize identifier=_identifier;
// - (void).cxx_destruct;
- (id)detectedKeywordsDictionary;
- (void)addDetectedKeyword:(id)arg1 classificationTypeIdentifier:(id)arg2;
@property(readonly) NSString *lowercaseSubject;
@property(retain, nonatomic) NSArray *messageUnits;
- (void)addMessageUnit:(id)arg1;
- (id)initWithHTMLContent:(id)arg1 emailHeadersDictionary:(id)arg2 dateSent:(id)arg3;
- (id)firstHeaderValueForKey:(id)arg1 inHeaders:(id)arg2;
- (id)initWithIdentifier:(id)arg1 subject:(id)arg2 sender:(id)arg3 recipients:(id)arg4 dateSent:(id)arg5;
- (id)initWithDateSent:(id)arg1 subject:(id)arg2;
- (id)initWithDateSent:(id)arg1;
- (id)initWithIdentifier:(id)arg1 subject:(id)arg2 sender:(id)arg3 recipients:(id)arg4 dateSent:(id)arg5 type:(id)arg6;
- (id)init;

@end
