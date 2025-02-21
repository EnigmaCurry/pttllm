import serial
import time
import logging
logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

serial_port = '/dev/ttyUSB0'

ser = serial.Serial(serial_port)

def ptt_on():
    ser.setDTR(True)
    log.info("PTT ON")

def ptt_off():
    ser.setDTR(False)
    log.info("PTT OFF")

