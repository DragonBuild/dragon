//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//


@class CNSaveRequest;

@protocol DACardDAVRecord <NSObject>
- (void)markForDeletion;
- (void)updateSaveRequest:(CNSaveRequest *)arg1;
- (BOOL)isAccount;
- (BOOL)isContainer;
- (BOOL)isGroup;
- (BOOL)isContact;
@end
