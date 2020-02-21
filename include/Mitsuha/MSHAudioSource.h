#import "MSHAudioDelegate.h"

@interface MSHAudioSource : NSObject

@property (nonatomic, assign) bool isRunning;
@property (nonatomic, retain) id<MSHAudioDelegate> delegate;

-(id)init;
-(void)start;
-(void)stop;

@end