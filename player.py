import threading
from time import sleep

class Player(threading.Thread):
    def __init__(self, logger, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.logger = logger
        self.logger.debug("Player object created")

    def run(self):
        while True:
            try:
                msg = self.queue.get()
                self.logger.debug("Player got message from queue " + str(msg))

            except Exception as e:
                self.logger.exception("Exception in player thread: " + str(e))

            sleep(0.5)
        logger.warn("Exiting player thread")
