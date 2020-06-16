#import <UIKit/UIKit.h>
#import "MSHJelloLayer.h"
#import "MSHView.h"

@interface MSHJelloView : MSHView

@property (nonatomic, strong) MSHJelloLayer *waveLayer;
@property (nonatomic, strong) MSHJelloLayer *subwaveLayer;

-(CGPathRef)createPathWithPoints:(CGPoint *)points pointCount:(NSUInteger)pointCount inRect:(CGRect)rect;

@end
