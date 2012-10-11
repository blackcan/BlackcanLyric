#import "AutoFindLyric.h"
#import <EyeTunes/EyeTunes.h>

@implementation AutoFindLyric
- (IBAction)fetch:(id)sender {
	EyeTunes *e = [EyeTunes sharedInstance];
	ETTrack *t = [e currentTrack];
	
	NSString *singer = [t artist];
	NSString *song = [t name];
	NSString *finalLyric;

	lastSinger = singer;
	lastSong = song;
	
	NSURL *url;
	NSData *data;
	
	url = [NSURL URLWithString:[[NSString stringWithFormat:@"http://blackcanlyrics.appspot.com/?singer=%@&song=%@", singer, song] stringByAddingPercentEscapesUsingEncoding:NSUTF8StringEncoding]];
	data = [url resourceDataUsingCache: NO];
	finalLyric = [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
	
	[t setLyrics:finalLyric];
	[Singer setStringValue:singer];
	[Song setStringValue:song];
	finalLyric = [t lyrics];
	[Lyric setString:finalLyric];
}

-(void)getLyric
{
	EyeTunes *e = [EyeTunes sharedInstance];
	ETTrack *t = [e currentTrack];
	
	NSString *singer = [t artist];
	NSString *song = [t name];
	NSString *finalLyric;
	
	if((singer != lastSinger || song != lastSong))
	{
		if([[t lyrics] isEqualToString:@""])
		{
			lastSinger = singer;
			lastSong = song;
			
			NSURL *url;
			NSData *data;
			
			url = [NSURL URLWithString:[[NSString stringWithFormat:@"http://blackcanlyrics.appspot.com/?singer=%@&song=%@", singer, song] stringByAddingPercentEscapesUsingEncoding:NSUTF8StringEncoding]];
			data = [url resourceDataUsingCache: NO];
			finalLyric = [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
			
			[t setLyrics:finalLyric];
			
		}
		[Singer setStringValue:singer];
		[Song setStringValue:song];
		finalLyric = [t lyrics];
		[Lyric setString:finalLyric];
	}
}

-(void)awakeFromNib
{
	SEL mySelector = @selector(getLyric);
	[NSTimer scheduledTimerWithTimeInterval:1.0 target:self selector:mySelector userInfo:nil repeats:YES]; 	
}
@end
