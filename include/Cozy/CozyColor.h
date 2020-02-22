@interface CozyColor : NSObject

- (instancetype)initWithRed:(CGFloat)red green:(CGFloat)green blue:(CGFloat)blue;

@property (nonatomic, assign) CGFloat h;
@property (nonatomic, assign) CGFloat s;
@property (nonatomic, assign) CGFloat v;
@property (nonatomic, assign) CGFloat r;
@property (nonatomic, assign) CGFloat g;
@property (nonatomic, assign) CGFloat b;
@property (nonatomic, assign) CGFloat a;

- (UIColor *)getColor; 

@end