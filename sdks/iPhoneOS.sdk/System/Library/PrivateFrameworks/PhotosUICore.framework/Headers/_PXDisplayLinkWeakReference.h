//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@interface _PXDisplayLinkWeakReference : NSObject
{
    id _object;
    SEL _selector;
}

@property(readonly, nonatomic) SEL selector; // @synthesize selector=_selector;
@property(readonly, nonatomic) __weak id object; // @synthesize object=_object;
// - (void).cxx_destruct;
- (void)handleDisplayLink:(id)arg1;
- (id)initWithObject:(id)arg1 selector:(SEL)arg2;

@end
