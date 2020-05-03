//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//


@protocol SBAppSwitcherPageContentView <NSObject>
@property(nonatomic, getter=isVisible) BOOL visible;
@property(nonatomic, getter=isActive) BOOL active;
@property(readonly, nonatomic) BOOL contentRequiresGroupOpacity;
@property(nonatomic) long long orientation;
@property(nonatomic) double cornerRadius;
- (void)invalidate;

@optional
- (void)setShowingIconOverlayView:(BOOL)arg1;
- (void)setShouldUseBrightMaterial:(BOOL)arg1;
@end
