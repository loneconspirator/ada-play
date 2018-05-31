#!/usr/bin/python

import os
import Queue
from time import sleep
import traceback

import logger
from player import Player
from rfid_reader import RfidReader
from web_site import Server

logger = logger.get_logger()
queue = Queue.PriorityQueue()

def main():
    logger.info("Starting AdaPlay...")

    player = None
    rfid_reader = None
    web_site = None

    loops = 0
    while True:
        try:
            loops = loops + 1
            logger.debug("Main Loop " + str(loops))

            if not rfid_reader or not rfid_reader.is_alive():
                logger.info("Starting rfid_reader thread")
                rfid_reader = RfidReader(logger, queue)
                rfid_reader.setDaemon(True)
                rfid_reader.start()

            if not player or not player.is_alive():
                logger.info("Starting player thread")
                player = Player(logger, queue)
                player.setDaemon(True)
                player.start()

            if not web_site or not web_site.is_alive():
                logger.info("Sterting web_site thread")
                web_site = Server(logger, queue)
                web_site.setDaemon(True)
                web_site.start()

        except Exception as e:
            logger.exception("Exception in main thread: " + str(e))

        sleep(15)

    logger.warn("Exiting main thread")

if __name__ == '__main__':
    main()
