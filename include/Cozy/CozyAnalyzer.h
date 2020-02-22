#include "CozySchema.h"
@interface CozyAnalyzer : NSObject

+ (CozySchema *)schemaForImage:(UIImage *)image withOptions:(NSArray *)options;

@end