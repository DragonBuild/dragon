//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

@class NSArray;

@protocol FontProviderProtocol
- (void)registeredFontsInfo:(BOOL)arg1 completionHandler:(void (^)(NSArray *))arg2;
- (void)unregisterFonts:(NSArray *)arg1 completionHandler:(void (^)(NSArray *, NSDictionary *))arg2;
- (void)registerFonts:(NSArray *)arg1 enabled:(BOOL)arg2 completionHandler:(void (^)(NSArray *, NSDictionary *))arg3;
@end
