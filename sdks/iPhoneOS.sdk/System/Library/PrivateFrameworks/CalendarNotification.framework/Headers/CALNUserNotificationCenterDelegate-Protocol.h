//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

@class CALNNotification, CALNNotificationResponse;
@protocol CALNUserNotificationCenter;

@protocol CALNUserNotificationCenterDelegate
- (void)userNotificationCenter:(id <CALNUserNotificationCenter>)arg1 didReceiveNotificationResponse:(CALNNotificationResponse *)arg2 withCompletionHandler:(void (^)(void))arg3;
- (void)userNotificationCenter:(id <CALNUserNotificationCenter>)arg1 willPresentNotification:(CALNNotification *)arg2 withCompletionHandler:(void (^)(NSUInteger))arg3;
@end
