import threading
from time import sleep

try:
    import MFRC522
    MIFAREReader = MFRC522.MFRC522()
    import RPi.GPIO as GPIO
    PI = True
except:
    PI = False

class RfidReader(threading.Thread):
    def __init__(self, logger, queue):
        threading.Thread.__init__(self)
        self.logger = logger
        self.queue = queue
        self.logger.debug("RfidReader object created")

    def run(self):
        while True:
            try:
                card_id = self.get_card_id()
                if card_id:
                    self.logger.debug("Read card_id: " + str(card_id))
                    # Add to queue
                    self.queue.put((card_id, "hi"))
                sleep(0.5)

            except Exception as e:
                self.logger.exception("Exception in RfidReader thread: " + str(e))

        logger.warn("Exiting RfidReader thread")

    def strip_byte(self, byte):
        return hex(byte)[2:4]

    def string_for_bytes(self, bytes):
        return '-'.join(map(self.strip_byte, bytes))

    def get_card_id(self):
        if PI:
            self.logger.debug("Reading from RFID")
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                card_id = self.string_for_bytes(uid)
                self.logger.debug("Got something from RFID!: " + card_id)
                return card_id
            else:
                self.logger.debug("Nothing from RFID")
                return None
        else:
            sleep(2.5)
            return "foo"

