@protocol MSHAudioProcessingDelegate <NSObject>

- (void)setSampleData:(float *)data length:(int)length;

@end