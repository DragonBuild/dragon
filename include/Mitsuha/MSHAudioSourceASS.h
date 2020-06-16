#import "MSHAudioSource.h"

#define ASSPort 43333

@interface MSHAudioSourceASS : MSHAudioSource {
    int connfd;
    float *empty;
    bool forceDisconnect;
}

@end