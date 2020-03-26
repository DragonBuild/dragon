//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@protocol UICoordinateSpace;

@interface PXViewLayoutHelper : NSObject
{
    CGRect _containerBounds;
    id <UICoordinateSpace> _coordinateSpace;
    CGAffineTransform _transform;
    CGAffineTransform _reverseTransform;
}

+ (void)performLayoutWithinView:(id)arg1 usingBlock:(id /* CDUnknownBlockType */)arg2;
+ (void)setUserInterfaceLayoutDirection:(long long)arg1;
+ (long long)userInterfaceLayoutDirection;
+ (void)initialize;
// - (void).cxx_destruct;
- (void)_getFirstBaseline:(double )arg1 lastBaseline:(double )arg2 forView:(id)arg3 withSize:(CGSize)arg4;
- (void)_setOrientedFrame:(CGRect)arg1 forView:(id)arg2;
- (CGRect)_orientedFrameOfView:(id)arg1;
- (void)_tearDown;
- (void)_setUpWithView:(id)arg1;
- (double)lastBaselineOfView:(id)arg1;
- (double)firstBaselineOfView:(id)arg1;
- (double)bottomOfView:(id)arg1;
- (double)verticalCenterOfView:(id)arg1;
- (double)topOfView:(id)arg1;
- (double)trailingOfView:(id)arg1;
- (double)horizontalCenterOfView:(id)arg1;
- (double)leadingOfView:(id)arg1;
- (void)layoutView:(id)arg1 withAttributes:(const CDStruct_05cddbcc )arg2;
- (id)_init;
- (id)init;

@end
