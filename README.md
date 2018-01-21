# Ada Play
A pi based RFID music player for toddlers.

Intended to be run from a Pi Zero W in an enclosure with a RFID reader. It run a local media server, so you put music files on the pi's local disk and map RFID chips to those files. It will play over AirPlay.

My first project with Raspberry Pi or Python.

## Setup

Connect an RFID reader and download the software as described in [this guide](http://www.instructables.com/id/RFID-RC522-Raspberry-Pi/)

### Setup software on the pi
#### Install Raspbian using NOOBS
Make sure to open ssh connections and change the password for the `pi` user from `raspberry`

change the hostname to be `ada-play`

#### Install this ada-play script as a daemon
TODO: put the git clone command in here
`sudo cp ada-play/ada-play.sh /etc/init.d/`
`sudo chown root:root /etc/init.d/ada-play.sh`
`sudo chmod 755 /etc/init.d/ada-play.sh`

#### Put some music on to your server
You can use SFTP or SCP and drop songs into `/home/pi/Music`

#### forked-daapd
This is the daemon that makes the pi into a media server that can talk to AirPlay targets, and be controlled by iTunes remotes

* Install [forked-daapd](https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=49928&hilit=itunes)
* Configure forked-daapd
    - `ssh pi@ada-play.local`
    - edit `/etc/forked-daapd.conf`
    - point to library `/home/pi/Music` (line 71)
    - talk to airplay server (line 224, set password line 234)
    - have an admin password for the web ui (probably a good idea) (line 27)
    - Set the device name (line 186)
* Start the daemon
    - `sudo service forked-daapd start`
    - configure daemon to start at boot
    - Open rc.local as root `sudo nano /etc/rc.local`
    - Put this above the exit line: `service forked-daapd start`
* Configure the setup
    - Visit the forked-daapd web ui http://forked-daapd.local:3689/admin.html
    - Log in with uid `admin` and the password you set above
    - Click "Update Library" to scan your music folder
    - Select the target speakers in the "Outputs" section
    - Connect to ada-play preferably using the "Remote" app on a phone and verify you can play music over the speaker you've connected to ada-play

* Install mpc
    - `sudo apt install mpc`

