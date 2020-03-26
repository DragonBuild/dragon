//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

#import <FamilyCircleUI/AAUISpecifierProvider-Protocol.h>
#import <FamilyCircleUI/FAFamilySettingsViewControllerDelegate-Protocol.h>
#import <FamilyCircleUI/FASetupDelegate-Protocol.h>
#import <FamilyCircleUI/RemoteUIControllerDelegate-Protocol.h>

@class AAFamilyDetailsResponse, AAFamilyEligibilityResponse, AAGrandSlamSigner, AIDAAccountManager, FACircleContext, FAFamilyMemberDetailsPageSurrogate, FAFamilyNotificationObserver, FARequestConfigurator, NSArray, NSMutableArray, NSOperationQueue, NSString, PSListController, PSSpecifier;
@protocol AAUISpecifierProviderDelegate;

@interface FASettingsSpecifierProvider : NSObject <FASetupDelegate, FAFamilySettingsViewControllerDelegate, RemoteUIControllerDelegate, AAUISpecifierProvider>
{
    FAFamilyMemberDetailsPageSurrogate *_profileSurrogate;
    FAFamilyNotificationObserver *_familyNotificationObserver;
    PSListController *_presenter;
    PSSpecifier *_familyCellSpecifier;
    PSSpecifier *_invitationsCellSpecifier;
    BOOL _isLoadingFamilyDetails;
    BOOL _didFailToGetFamilyDetails;
    NSMutableArray *_pendingFamilyDetailsCompletionBlocks;
    AAFamilyDetailsResponse *_familyDetailsResponse;
    AAFamilyEligibilityResponse *_familyEligibilityResponse;
    NSMutableArray *_pendingInvites;
    NSString *_familyStatusSummary;
    NSString *_invitationSummary;
    long long _familyEligibilityStatus;
    BOOL _isHandlingURLForInvite;
    NSOperationQueue *_networkActivityQueue;
    AIDAAccountManager *_accountManager;
    AAGrandSlamSigner *_grandSlamSigner;
    FARequestConfigurator *_requestConfigurator;
    FACircleContext *_context;
    BOOL _delayedEnterInitiateFlow;
    id <AAUISpecifierProviderDelegate> _delegate;
    NSArray *_specifiers;
}

@property(nonatomic) __weak id <AAUISpecifierProviderDelegate> delegate; // @synthesize delegate=_delegate;
// - (void).cxx_destruct;
- (void)dealloc;
- (void)_handleObjectModelChangeForController:(id)arg1 objectModel:(id)arg2 isModal:(BOOL)arg3;
- (void)remoteUIController:(id)arg1 willPresentObjectModel:(id)arg2 modally:(BOOL)arg3;
- (void)remoteUIController:(id)arg1 didRefreshObjectModel:(id)arg2;
- (BOOL)remoteUIController:(id)arg1 shouldLoadRequest:(id)arg2 redirectResponse:(id)arg3;
- (void)_handleStartFamilySetupActionURL:(id)arg1;
- (void)_handleShowInviteActionURL:(id)arg1 isChildTransfer:(BOOL)arg2;
- (void)_handleShowFamilyInviteActionURL:(id)arg1;
- (void)_handleShowChildTransferActionURL:(id)arg1;
- (id)_acuPresenter;
- (void)_handleShowFamilySettingsURL:(id)arg1;
- (void)_handleShowInvitesActionURL:(id)arg1;
- (BOOL)handleURL:(id)arg1;
- (void)_clearFamilyState;
- (void)familySettingsViewControllerDidUpdateFamily:(id)arg1;
- (void)familySettingsViewControllerDidDeleteFamily:(id)arg1;
- (void)_reloadFamilySpecifiersAnimated:(BOOL)arg1;
- (void)_reloadFamilySpecifiers;
- (void)reloadSpecifiers;
- (void)_handleFamilyEligibilityResponse:(id)arg1 completion:(id /* CDUnknownBlockType */)arg2;
- (void)_loadFamilyEligibilityWithCompletion:(id /* CDUnknownBlockType */)arg1;
- (void)_viewFamilySpecifierWasTapped:(id)arg1;
- (id)_valueForFamilySpecifier:(id)arg1;
- (void)_presentPendingInvitesRemoteUI;
- (void)_pendingInvitationsSpecifierWasTapped:(id)arg1;
- (id)_valueForInvitiationsSpecifier:(id)arg1;
- (void)familySetupViewController:(id)arg1 didCompleteWithSuccess:(BOOL)arg2;
- (void)_showUnderageAlertWithEligibilityResponse:(id)arg1;
- (id)_configureContextWithType:(id)arg1 resourceDictionary:(id)arg2;
- (void)_initiateFamilyWithResources:(id)arg1;
- (void)_initiateFamily;
- (void)_reloadFamily;
- (void)_setUpFamilySpecifierWasTapped:(id)arg1;
- (void)_handleFamilyDetailsResponse:(id)arg1 completion:(id /* CDUnknownBlockType */)arg2;
- (void)_loadFamilyDetailsWithCompletion:(id /* CDUnknownBlockType */)arg1;
- (id)_familySpecifier;
- (id)_invitationsCellSpecifier;
- (NSUInteger)_familyState;
@property(copy, nonatomic) NSArray *specifiers; // @synthesize specifiers=_specifiers;
- (BOOL)_isEnabled;
- (id)_requestConfigurator;
- (id)_grandSlamSigner;
- (id)_appleAccount;
- (id)_accountStore;
- (id)initWithAccountManager:(id)arg1 presenter:(id)arg2;
- (id)initWithAccountManager:(id)arg1;

@end
