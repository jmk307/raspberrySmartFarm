import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

def panon():
  try:
    while True:
      GPIO.output(21, GPIO.HIGH)
      time.sleep(500)
      GPIO.output(21, GPIO.LOW)
      time.sleep(500)
    GPIO.cleanup()
  except KeyboardInterrupt:
      pass

panon()