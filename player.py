import threading
from time import sleep
from datetime import datetime
from subprocess import check_output
import json

def load_songs():
    songs_data = open("/home/pi/ada-play/songs.json").read()
    return json.loads(songs_data)

class Player(threading.Thread):
    def __init__(self, logger, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.logger = logger
        self.logger.debug("Player object created")
        self.current_card = None
        self.last_message_time = None

    def run(self):
        while True:
            try:
                msg = self.queue.get()
                self.logger.debug("Player got message from queue " + str(msg))
                self.try_song(msg[0])
            except Exception as e:
                self.logger.exception("Exception in player thread: " + str(e))
            sleep(0.5)
        logger.warn("Exiting player thread")

    def try_song(self, card_id):
        curtime = datetime.now()
        if card_id == self.current_card:
            return
        timestamp = curtime.strftime('%Y-%m-%d %H:%M:%S')
        self.current_card = card_id
        self.last_message_time = curtime
        songs = load_songs()
        if card_id in songs:
            self.logger.debug("Playing song %s" % songs[card_id])
            # Here I would write to my actual log of songs played
            self.play(songs[card_id])
        else:
            self.logger.debug("Encountered unknown card: %s" % card_id)

    def play(self, name):
        self.mpc('stop')
        self.mpc('clear')
        self.mpc('add', 'file:/home/pi/Music/%s' % name)
        self.mpc('play')

    def mpc(self, *args):
        check_output(['mpc'] + list(args))
