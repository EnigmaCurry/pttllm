import serial
import time
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

serial_port = '/dev/ttyUSB0'
ser = None  # Serial port will be initialized when needed

def init_serial():
    global ser
    if ser is None:
        ser = serial.Serial(serial_port)
        log.info(f"Initialized serial port: {serial_port}")

def ptt_on():
    init_serial()
    ser.setRTS(True)
    log.info("PTT ON")

def ptt_off():
    init_serial()
    ser.setRTS(False)
    log.info("PTT OFF")
