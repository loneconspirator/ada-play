#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
from subprocess import check_output

from datetime import datetime
import signal
import json

continue_reading = True

current_card = ""

def load_songs():
    songs_data = open("songs.json").read()
    return json.loads(songs_data)

songs = load_songs()

def try_song(card_id):
    global current_card
    curtime = datetime.now()
    # print "comparing: ", card_id, current_card
    if card_id == current_card:
        return
    timestamp = curtime.strftime('%Y-%m-%d %H:%M:%S')
    current_card = card_id
    if card_id in songs:
        print timestamp, " Playing ", songs[card_id]
        start_song(songs[card_id])
    else:
        print timestamp, " Unknown ID: " + card_id

def run_and_wait(cmd):
    return check_output(cmd)

def start_song(name):
    run_and_wait(['mpc', 'stop'])
    run_and_wait(['mpc', 'clear'])
    run_and_wait(['mpc', 'add', 'file:/home/pi/Music/%s' % name])
    run_and_wait(['mpc', 'play'])


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

def strip_byte(byte):
    return hex(byte)[2:4]

def string_for_bytes(bytes):
    return '-'.join(map(strip_byte, bytes))

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
print "Started ada-play"

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    # if status == MIFAREReader.MI_OK:
    #     print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        card_id = string_for_bytes(uid)
        # print "Card read UID: " + card_id
        try_song(card_id)
