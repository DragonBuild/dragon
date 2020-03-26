//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <ProtocolBuffer/PBCodable.h>

#import <EmailDaemon/EDPETMessageFrameTypeIntrospectable-Protocol.h>

@interface EDPETQuotaReachedEvent : PBCodable <EDPETMessageFrameTypeIntrospectable, NSCopying>
{
    NSUInteger _droppedEventsCount;
    NSUInteger _timestamp;
    unsigned int _sequenceNumber;
    int _timezoneOffset;
    struct {
        unsigned int droppedEventsCount:1;
        unsigned int timestamp:1;
        unsigned int sequenceNumber:1;
        unsigned int timezoneOffset:1;
    } _has;
}

@property(nonatomic) NSUInteger droppedEventsCount; // @synthesize droppedEventsCount=_droppedEventsCount;
@property(nonatomic) int timezoneOffset; // @synthesize timezoneOffset=_timezoneOffset;
@property(nonatomic) unsigned int sequenceNumber; // @synthesize sequenceNumber=_sequenceNumber;
@property(nonatomic) NSUInteger timestamp; // @synthesize timestamp=_timestamp;
- (void)mergeFrom:(id)arg1;
- (NSUInteger)hash;
- (BOOL)isEqual:(id)arg1;
// - (id)copyWithZone:(_NSZone )arg1;
- (void)copyTo:(id)arg1;
- (void)writeTo:(id)arg1;
- (BOOL)readFrom:(id)arg1;
- (id)dictionaryRepresentation;
- (id)description;
@property(nonatomic) BOOL hasDroppedEventsCount;
@property(nonatomic) BOOL hasTimezoneOffset;
@property(nonatomic) BOOL hasSequenceNumber;
@property(nonatomic) BOOL hasTimestamp;
- (int)messageFrameType;

@end
