//
//  timer.m
//  AutoFindLyric
//
//  Created by blackcan on 2011/3/24.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "timer.h"
#import "AutoFindLyric.h"


@implementation timer
-(void)myTimerCallback:(NSTimer *)timer
{
	NSLog(@"tick");
	[findLyric getLyric];
}
- (void)awakeFromNib
{
	SEL mySelector = @selector(myTimerCallback:);
	[NSTimer scheduledTimerWithTimeInterval:10.0 target:self selector:mySelector userInfo:nil repeats:YES];    
}
@end
