#import <UIKit/UIKit.h>
#import "MSHView.h"
#import "MSHJelloLayer.h"

@interface MSHLineView : MSHView

@property (nonatomic, assign) CGFloat lineThickness;
@property (nonatomic, strong) MSHJelloLayer *waveLayer;

-(CGPathRef)createPathWithPoints:(CGPoint *)points pointCount:(NSUInteger)pointCount inRect:(CGRect)rect;

@end