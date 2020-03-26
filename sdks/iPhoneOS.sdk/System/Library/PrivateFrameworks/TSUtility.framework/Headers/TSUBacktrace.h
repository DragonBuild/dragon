//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@interface TSUBacktrace : NSObject
{
    void _callstack;
    int _frames;
    int _initAdjustment;
}

+ (id)callee;
+ (id)caller;
+ (id)new;
+ (id)backtrace;
- (BOOL)isEqual:(id)arg1;
- (id)callee;
- (id)caller;
- (id)callerAtIndex:(long long)arg1;
- (id)backtraceString;
- (void)dealloc;
- (id)init;
- (id)initWithAdjustment:(int)arg1;

@end
