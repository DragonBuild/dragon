//
//     Generated by class-dump 3.5 (64 bit) (Debug version compiled Mar 22 2020 01:47:48).
//
//  Copyright (C) 1997-2019 Steve Nygard.
//

#import <objc/NSObject.h>

@interface YahooResponseParser : NSObject
{
}

+ (void)parseStockQuoteDictionaries:(id)arg1 withDataSources:(id)arg2 parsedStockResult:(id /* CDUnknownBlockType */)arg3;
+ (void)parseExchangeDictionaries:(id)arg1 parsedExchangeResult:(id /* CDUnknownBlockType */)arg2;
+ (id)parseDataSourceMapFromDataSourceDictionaries:(id)arg1;
+ (void)parseData:(id)arg1 resultsHandler:(id /* CDUnknownBlockType */)arg2;
+ (id)objectOfClass:(Class)arg1 withDictionaryKeyPath:(id)arg2 inJSONObject:(id)arg3;
+ (id)arrayWithDictionaryKeyPath:(id)arg1 inJSONObject:(id)arg2 wrapResultIfDictionary:(BOOL)arg3;
+ (id)dictionaryWithDictionaryKeyPath:(id)arg1 inJSONObject:(id)arg2;
+ (id)objectWithDictionaryKeyPath:(id)arg1 inJSONObject:(id)arg2;

@end
