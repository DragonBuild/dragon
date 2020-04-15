#import <Preferences/PSListController.h>

@interface ExampleRootListController : PSListController

@end

@implementation ExampleRootListController

- (NSArray *)specifiers {
	if (!_specifiers) {
		_specifiers = [self loadSpecifiersFromPlistName:@"Root" target:self];
	}

	return _specifiers;
}

@end
