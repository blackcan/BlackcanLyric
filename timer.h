//
//  timer.h
//  AutoFindLyric
//
//  Created by blackcan on 2011/3/24.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "AutoFindLyric.h"

@interface timer : NSObject {
	
	AutoFindLyric *findLyric;
}
-(void)awakeFromNib;
-(void)myTimerCallback:(NSTimer *)timer;
@end
