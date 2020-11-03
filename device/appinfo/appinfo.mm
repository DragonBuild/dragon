// creative commons blah blah
// @krit nov 2020

@import Foundation;
#include <objc/runtime.h>
#include <dlfcn.h>
#include <CoreServices/CoreServices.h>
#include <unistd.h>

@interface LSApplicationProxy : NSObject
@property (nonatomic, retain) NSString *itemName;
@property (nonatomic, retain) NSString *applicationIdentifier;
@property (nonatomic, retain) NSString *bundleExecutable;
@property (nonatomic, retain) NSURL *dataContainerURL;
@property (nonatomic, retain) NSString *canonicalExecutablePath;
@end


NSMutableArray *apps;

NSString *idToExecutable(char *bundle);
NSString *idToPath(char *bundle);
NSString *idToContainer(char *bundle);

void pout(NSString *out)
{
     printf([out UTF8String]);
}

int main(int argc, char *argv[])
{
    dlopen("/System/Library/Frameworks/CoreServices.framework/CoreServices", 0x4);
    Class LSApplicationWorkspace_class = objc_getClass("LSApplicationWorkspace");
    //Class LSApplicationProxy_class = objc_getClass("LSApplicationProxy");
    SEL selector = NSSelectorFromString(@"defaultWorkspace");
    NSObject* workspace = [LSApplicationWorkspace_class performSelector:selector];
    SEL selectorALL = NSSelectorFromString(@"allInstalledApplications");

    apps = [workspace performSelector:selectorALL];


    
    if (strncmp(argv[1], "-e", 2) == 0)
        pout(idToExecutable(argv[2]));
    if (strncmp(argv[1], "-p", 2) == 0)
        pout(idToPath(argv[2]));
    if (strncmp(argv[1], "-c", 2) == 0)
        pout(idToContainer(argv[2]));
    
}


NSString *idToExecutable(char *bundle)
{
    for (LSApplicationProxy *app in apps)
    {
        if ([app.applicationIdentifier isEqualToString:[NSString stringWithUTF8String:bundle]])
        return app.bundleExecutable;
    }
}

NSString *idToPath(char *bundle)
{
    for (LSApplicationProxy *app in apps)
    {
        if ([app.applicationIdentifier isEqualToString:[NSString stringWithUTF8String:bundle]])
        return app.canonicalExecutablePath;
    }
}

NSString *idToContainer(char *bundle)
{
    for (LSApplicationProxy *app in apps)
    {
        if ([app.applicationIdentifier isEqualToString:[NSString stringWithUTF8String:bundle]])
        return app.dataContainerURL.absoluteString;
    }
}
