#include "CozyColor.h"

@interface CozySchema : NSObject

//  A bit complex yet not so much
//  I use this to flip individual bits to declare
//      what colors were found and what were generated
//
//  I've documented it in the README for this project
//  You *probably* dont need this. 
@property (nonatomic, assign) char foundColors;

@property (nonatomic, retain) NSArray *options;

@property (nonatomic, assign) BOOL darker;

//  Primary Label color, for song name
@property (nonatomic, retain) CozyColor *labelColor;
//  Darker secondary label color, for album/artist and time control colors
@property (nonatomic, retain) CozyColor *secondaryLabelColor;
//  Even darker label for unimportant things
@property (nonatomic, retain) CozyColor *tertiaryLabelColor;

//  Lightest, white-tinted color for larger controls and knobs
@property (nonatomic, retain) CozyColor *controlColor;
//  Darker secondary color for active slider portions and time controls
@property (nonatomic, retain) CozyColor *secondaryControlColor;
//  Near-background color for unactive (right side) slider portions
@property (nonatomic, retain) CozyColor *tertiaryControlColor;

//  Most contrasting color in the image
@property (nonatomic, retain) CozyColor *contrastColor;

//  Most Common color in the image
@property (nonatomic, retain) CozyColor *commonColor;

//  Generated background color
@property (nonatomic, retain) CozyColor *backgroundColor;

+ (CozySchema *)generateFromImage:(UIImage *)image withOptions:(NSArray *)options;
//  These are methods used by CozySchema. 
//  I've left them public since they may be of use in other projects. 

- (BOOL)brightnessIsTooLow:(CozyColor *)color;

- (BOOL)saturationIsTooLow:(CozyColor *)color;

+ (CozyColor *)lighterColorForColor:(CozyColor *)c byFraction:(CGFloat)frac;

+ (CozyColor *)darkerColorForColor:(CozyColor *)c byFraction:(CGFloat)frac;

@end