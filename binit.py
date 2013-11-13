#!/usr/bin/python
import os
def main():
	print('You probably want to run this on the client that will be holding the downloaded media\n');
	print('If you dont have seperate watch directories for trackers / media then you are a slob and probably wont find much value in this.\n');
	LUSER = raw_input('Enter the username for the media server / NAS / your machine: ');
	LIP = raw_input('Local WAN Address / DNS: ');
	RUSER = raw_input('Enter the remote users name of the server running rtorrent: ');
	RHOST = raw_input('Enter the hostname / ip of the server running rtorrent: ');
	rtline = "system.method.set_key=event.download.finished,move_complete,\"execute=ssh," + LUSER + "@" + LIP + ",/home/" + LUSER + "/bsync.sh;\"";
	print('#####################################################################\n');
	print("Put this line at the bottom of your ~/.rtorrent.rc \n" + rtline +"\n");	
	print('#####################################################################\n');
	print('You will need to make sure that your remote server has ssh keys built and that they are copied to your local machines authorized keys.');
	print('The easiest way to do this to run \'ssh-keygen\' on the remote machine, and pressing enter for all of the defaults.');
	print("Afterward, copy the ssh key of the remote machine to your local ssh/media server.");
	print("The easiest way to do this to execute the following on the remote machine \'ssh-copy-id -i ~/.ssh/id_rsa.pub " + LUSER+"@"+LIP+" \'");
	print('At this point, a seamless ssh connection can be made from the remote machine to your local machine which holds or even plays the media.');
	print('\n#####################################################################');
	
	f = open("/home/"+LUSER+"/bsync.sh",'w');
	f.write("#!/bin/bash\n\n");
	f.write("####### Put as many local variables as you have here, for example movies, music, tv, books, etc.#######\n\n");
	f.write("echo \"I was executed: $(date)\" >> ~/.bsynclog\n");
	f.write("REMOTE1=/home/"+ RUSER + "/torrents/music/downloads/\n");
	f.write("LOCAL1=/home/" + LUSER + "/music/\n\n");
	f.write("REMOTE2=/home/"+ RUSER + "/torrents/tv/downloads/\n");
	f.write("LOCAL2=/home/" + LUSER + "/tvshows/\n\n");
	f.write("rsync -av "+ RUSER + "@" + RHOST + ":$REMOTE1 $LOCAL1 >> ~/.bsynclog\n");
	f.write("rsync -av "+ RUSER + "@" + RHOST + ":$REMOTE2 $LOCAL2 >> ~/.bsynclog\n");
	
	print('The rsync wrapping script template was created and saved in your home directory. This is the file that rtorrent will call when a file is down downloading.');
	print('If you wish to change its name or location, please make sure to edit the .rtorrent.rc on the rtorrent machine appropriately.');
	os.chmod("/home/"+LUSER+"/bsync.sh",0755);
	print('~/bsync.sh is now executable, make sure to edit it to point to the appropriate place.');
	print('When you have configured the ~/bsync.sh script to your liking, restart rtorrent. The next downloaded torrent will now follow the rules layed out by your ~/bsync.sh script.\n');
	print('Common errors are not running an ssh server locally(including having ports forwarded), not having the script named and edited properly, or having it non-executable.\n');
main();
