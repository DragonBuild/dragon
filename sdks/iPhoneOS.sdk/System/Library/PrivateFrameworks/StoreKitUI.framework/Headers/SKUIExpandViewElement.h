//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <StoreKitUI/SKUIViewElement.h>

__attribute__((visibility("hidden")))
@interface SKUIExpandViewElement : SKUIViewElement
{
    BOOL _open;
    BOOL _previousIsOpen;
}

@property(nonatomic) BOOL previousIsOpen; // @synthesize previousIsOpen=_previousIsOpen;
@property(readonly, nonatomic, getter=isOpen) BOOL open; // @synthesize open=_open;
- (long long)pageComponentType;
- (id)applyUpdatesWithElement:(id)arg1;
- (id)initWithDOMElement:(id)arg1 parent:(id)arg2 elementFactory:(id)arg3;

@end
