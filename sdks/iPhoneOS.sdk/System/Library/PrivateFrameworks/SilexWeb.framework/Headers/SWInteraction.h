//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <SilexWeb/SWInteraction-Protocol.h>

@class NSString;

@interface SWInteraction : NSObject <SWInteraction>
{
    NSUInteger _type;
}

@property(readonly, nonatomic) NSUInteger type; // @synthesize type=_type;
@property(readonly, copy) NSString *description;
- (BOOL)isEqual:(id)arg1;
- (void)perform;
- (id)initWithType:(NSUInteger)arg1;

@end
