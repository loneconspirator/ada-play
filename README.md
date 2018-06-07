# Ada Play
A pi based RFID music player for toddlers.

Intended to be run from a Pi Zero W in an enclosure with a RFID reader. It run a local media server, so you put music files on the pi's local disk and map RFID chips to those files. It will play over AirPlay / Chromecast.

My first project with Raspberry Pi or Python.

## Setup

### Setup software on the pi
#### Install Raspbian using NOOBS
Follow [these instructions](https://www.raspberrypi.org/documentation/installation/noobs.md) to get noobs set up. Configure your WiFi and Install Raspian

When raspian boots for the first time, open a console and run `sudo raspi-config` and make the following changes:
 * Change 1) Password to one of your choosing. Write it somewhere
 * Change 2) Network Options -> N1) Hostname to `ada-play`
 * Change 3) Boot Options -> B1) Desktop / CLI to `Console Autologin`
 * Change 5) Interfacing Options -> P2) SSH to be enabled
 * Finish and restart

### Connect the RFID Reader
Connect an RFID reader to the pi and download the software as described in [this guide](http://www.instructables.com/id/RFID-RC522-Raspberry-Pi/)

Now your wifi should be set up and you can `ssh pi@ada-play.local` from another computer and connect with your password

#### Clone and set up the ada-play codebase to run as a daemon
```bash
git clone https://github.com/loneconspirator/ada-play.git
cd ada-play
./setup.sh
```

#### Put some music on to your server
You can use SFTP or SCP and drop songs into `/home/pi/Music`

#### forked-daapd
This is the daemon that makes the pi into a media server that can talk to AirPlay targets, and be controlled by iTunes remotes

* Install [forked-daapd](https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=49928&hilit=itunes) TODO: Make this hoop-jumping a shell script you can just run
* Configure forked-daapd
    - `ssh pi@ada-play.local`
    - edit the config file `sudo nano /etc/forked-daapd.conf`
    - point to library `/home/pi/Music` (line 71)
    - talk to airplay server (line 224, set password line 234)
    - have an admin password for the web ui (probably a good idea) (line 27)
    - Set the device name (line 186) `Ada Play Device` - this is for playing from HDMI / speakers connected locally
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

* Set the timezone for the pi so that logging timestamp will be localized
    - `sudo timedatectl set-timezone "America/Los_Angeles"`

    >>> import datetime
    >>> datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    '2018-02-12 00:38:37'
    >>> dt = datetime.datetime.now()


## Known issues:
 * python script will crash if the mpc command returns with an error exit status
 * Audio has gotten glitchy when python process runs away and gobbles up cpu
 * I've also seen audio getting glitchy when there wasn't a process going haywire and memory usage wasn't even that bad (but the pi was sluggish in the terminal)
 * It kind of appears that the python process takes up massive cpu normally
 * I should use a library like this to daemonize the process https://pypi.python.org/pypi/python-daemon/

