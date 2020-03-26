//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <Navigation/MNLocationProvider-Protocol.h>
#import <Navigation/MNLocationProviderDelegate-Protocol.h>

@class MNCoreLocationProvider, NSBundle, NSString;
@protocol MNLocationProviderDelegate;

@interface MNHybridLocationProvider : NSObject <MNLocationProviderDelegate, MNLocationProvider>
{
    NSUInteger _mode;
    double _desiredAccuracy;
    MNCoreLocationProvider *_coreLocationProvider;
    id <MNLocationProviderDelegate> _delegate;
}

@property(nonatomic) __weak id <MNLocationProviderDelegate> delegate; // @synthesize delegate=_delegate;
// - (void).cxx_destruct;
- (void)locationProvider:(id)arg1 didUpdateVehicleHeading:(double)arg2 timestamp:(id)arg3;
- (void)locationProvider:(id)arg1 didUpdateVehicleSpeed:(double)arg2 timestamp:(id)arg3;
- (void)locationProviderDidResumeLocationUpdates:(id)arg1;
- (void)locationProviderDidPauseLocationUpdates:(id)arg1;
- (BOOL)locationProviderShouldPauseLocationUpdates:(id)arg1;
- (void)locationProviderDidChangeAuthorizationStatus:(id)arg1;
- (void)locationProvider:(id)arg1 didReceiveError:(id)arg2;
- (void)locationProvider:(id)arg1 didUpdateHeading:(id)arg2;
- (void)locationProvider:(id)arg1 didUpdateLocation:(id)arg2;
@property(readonly, nonatomic) double timeScale;
@property(readonly, nonatomic) NSUInteger traceVersion;
@property(readonly, nonatomic) BOOL isTracePlayer;
@property(readonly, nonatomic) BOOL isSimulation;
@property(readonly, nonatomic) BOOL usesCLMapCorrection;
@property(nonatomic) long long activityType;
@property(readonly, nonatomic) int authorizationStatus;
@property(readonly, nonatomic) double expectedGpsUpdateInterval;
- (void)requestWhenInUseAuthorizationWithPrompt;
- (void)requestWhenInUseAuthorization;
@property(copy, nonatomic) id /* CDUnknownBlockType */ authorizationRequestBlock;
@property(nonatomic) int headingOrientation;
@property(nonatomic) BOOL matchInfoEnabled;
@property(nonatomic) double distanceFilter;
@property(nonatomic, getter=isLocationServicesPreferencesDialogEnabled) BOOL locationServicesPreferencesDialogEnabled;
@property(nonatomic) double desiredAccuracy;
@property(copy, nonatomic) NSString *effectiveBundleIdentifier;
@property(retain, nonatomic) NSBundle *effectiveBundle;
- (void)resetForActiveTileGroupChanged;
- (void)stopUpdatingVehicleHeading;
- (void)startUpdatingVehicleHeading;
- (void)stopUpdatingVehicleSpeed;
- (void)startUpdatingVehicleSpeed;
- (void)stopUpdatingHeading;
- (void)startUpdatingHeading;
- (void)stopUpdatingLocation;
- (void)startUpdatingLocation;
- (id)leechedLocationProvider;
- (id)coreLocationProvider;
- (void)_setEffectiveAccuracy:(double)arg1;
- (void)_sharedInit;
@property(nonatomic) NSUInteger mode;
- (id)initWithEffectiveBundleIdentifier:(id)arg1;
- (id)initWithEffectiveBundle:(id)arg1;
- (id)init;

@end
