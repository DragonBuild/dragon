#import <UIKit/UIKit.h>
#import "MSHAudioDelegate.h"
#import "MSHAudioProcessingDelegate.h"
#import "MSHAudioSource.h"
#import "MSHAudioProcessing.h"

@interface MSHView : UIView <MSHAudioDelegate, MSHAudioProcessingDelegate> {
    NSUInteger cachedLength;
    NSUInteger cachedNumberOfPoints;
    long long silentSince;
    long long lastUpdate;
    bool mshHidden;
    int bufferLog2;
    FFTSetup fftSetup;
    float* window;
}

@property (nonatomic, assign) BOOL shouldUpdate;
@property (nonatomic, assign) BOOL disableBatterySaver;
@property (nonatomic, assign) BOOL autoHide;
@property (nonatomic, assign) int numberOfPoints;

@property (nonatomic, assign) double gain;
@property (nonatomic, assign) double limiter;

@property (nonatomic, assign) CGFloat waveOffset;
@property (nonatomic, assign) CGFloat sensitivity;

@property (nonatomic, strong) CADisplayLink *displayLink;
@property (nonatomic, assign) CGPoint *points;

@property (nonatomic, strong) UIColor *calculatedColor;
@property (nonatomic, strong) UIColor *waveColor;
@property (nonatomic, strong) UIColor *subwaveColor;

@property (nonatomic, retain) MSHAudioSource *audioSource;
@property (nonatomic, retain) MSHAudioProcessing *audioProcessing;

-(void)updateWaveColor:(UIColor *)waveColor subwaveColor:(UIColor *)subwaveColor;

-(void)start;
-(void)stop;

-(void)configureDisplayLink;

-(void)initializeWaveLayers;
-(void)resetWaveLayers;
-(void)redraw;

-(void)updateBuffer:(float *)bufferData withLength:(int)length;

-(void)setSampleData:(float *)data length:(int)length;

-(instancetype)initWithFrame:(CGRect)frame;
-(instancetype)initWithFrame:(CGRect)frame audioSource:(MSHAudioSource *)audioSource;

@end
