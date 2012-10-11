#import <Cocoa/Cocoa.h>

@interface AutoFindLyric : NSObject {
    IBOutlet id Singer;
    IBOutlet id Song;
    IBOutlet id Lyric;
	NSString *lastSinger;
	NSString *lastSong;
}
- (IBAction)fetch:(id)sender;
-(void)awakeFromNib;
-(void)getLyric;
@end
