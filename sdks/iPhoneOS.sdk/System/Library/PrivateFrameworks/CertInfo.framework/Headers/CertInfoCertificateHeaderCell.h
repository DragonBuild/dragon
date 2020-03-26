//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <UIKit/UITableViewCell.h>

@class CertInfoGradientLabel, UIImage, UILabel;

@interface CertInfoCertificateHeaderCell : UITableViewCell
{
    UIImage *_certificateImage;
    UIImage *_notTrustedGradient;
    UILabel *_titleLabel;
    UILabel *_subtitleLabel;
    CertInfoGradientLabel *_trustedLabel;
}

// - (void).cxx_destruct;
- (void)layoutSubviews;
- (double)rowHeight;
- (void)setExpired:(BOOL)arg1;
- (void)setTrustSubtitle:(id)arg1;
- (void)setTrustTitle:(id)arg1;
- (id)_trustedLabel;
- (id)_notTrustedGradient;
- (id)_subtitleLabel;
- (id)_titleLabel;
- (id)_certificateImage;
- (id)initWithStyle:(long long)arg1 reuseIdentifier:(id)arg2;

@end
