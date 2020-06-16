#import <Accelerate/Accelerate.h>
#import "MSHAudioProcessingDelegate.h"

@interface MSHAudioProcessing : NSObject {
    int bufferLog2;
    FFTSetup fftSetup;
    float* window;
    UInt32 numberOfFrames;
    float fftNormFactor;
    int numberOfFramesOver2;
    float *outReal;
    float *outImaginary;
    COMPLEX_SPLIT output;
    float *out;
}

@property (nonatomic, assign) bool fft;
@property (nonatomic, retain) id<MSHAudioProcessingDelegate> delegate;

-(id)initWithBufferSize:(int)bufferSize;
-(void)process:(float *)data withLength:(int)length;

@end