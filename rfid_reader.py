import threading
from time import sleep

try:
    import MFRC522
    import RPi.GPIO as GPIO
    PI = True
except:
    PI = False

def strip_byte(byte):
    return hex(byte)[2:4]

def string_for_bytes(bytes):
    return '-'.join(map(strip_byte, bytes))

def getCardId():
    if PI:
        (status, uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            return string_for_bytes(uid)
        else:
            return None
    else:
        return "foo"

class RfidReader(threading.Thread):
    def __init__(self, logger, queue):
        threading.Thread.__init__(self)
        self.logger = logger
        self.queue = queue
        self.logger.debug("RfidReader object created")

    def run(self):
        while True:
            try:
                card_id = getCardId()
                if card_id:
                    self.logger.debug("Read card_id: " + str(card_id))
                    # Add to queue
                    self.queue.put((card_id, "hi"))
                sleep(2.5)

            except Exception as e:
                self.logger.exception("Exception in RfidReader thread: " + str(e))

        logger.warn("Exiting RfidReader thread")
