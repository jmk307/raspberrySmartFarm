import RPi.GPIO as GPIO   # 라즈베리파이 GPIO 모듈
import Adafruit_DHT       # 온습도 측정 센서 모듈
import time               # 시간 모듈

# LCD
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
E_PULSE = 0.0005
E_DELAY = 0.0005
GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT)  # RS
GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
GPIO.setup(LCD_D7, GPIO.OUT)  # DB7
# DHT11
sensor = Adafruit_DHT.DHT11
Celsius_pin = 27

# PAN
Transitor = 21
GPIO.setup(Transitor, GPIO.OUT)
GPIO.output(Transitor, GPIO.LOW)

# MOTOR
Survo_pin = 22
state = 0  # state == 1 -> ON, state == 0 -> OFF
GPIO.setup(Survo_pin, GPIO.OUT)
servoPWM = GPIO.PWM(Survo_pin, 50)
servoPWM.start(0)

# Data
Valid_temp = 0
Valid_humi = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 서보 모터 함수
def servo_on():  # 서보모터를 한사이클 돌림
    servoPWM.ChangeDutyCycle(9)
    time.sleep(0.5)
    servoPWM.ChangeDutyCycle(7)
    time.sleep(0.5)
    servoPWM.ChangeDutyCycle(9)

# 온습도 함수
def cel():  # 현재 스마트팜에 온습도를 측정
    humidity, temperature = Adafruit_DHT.read_retry(sensor, Celsius_pin)
    print("temperature:" + str(temperature))
    print("humidity: " + str(humidity))
    return humidity, temperature

# LCD 디스플레이 함수
def printDateTime():  # LCD에 현재 시간 출력
    textDate = strftime("%d %A %Y", gmtime())
    textTime = strftime("%H:%M:%S", gmtime())
    lcd_string(textDate, LCD_LINE_1)
    lcd_string(textTime, LCD_LINE_2)

def lcd_init():  # LCD 초기화
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):  # LCD 핀에 초기화 신호 전송
    GPIO.output(LCD_RS, mode)
# HIGH Data Bit
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    lcd_toggle_enable()
# LOW Data Bit
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    lcd_toggle_enable()

def lcd_toggle_enable():  # LCD 토글 설정
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):   # LCD에 String 출력
    message = str(message)
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


# 메임 함수
while True:
    # 웹에서 선택된 작물의 저장된 적정 온습도 읽음
    f = open("/var/www/html/temp.txt", 'r')
    f2 = open("/var/www/html/hum.txt", 'r')
    Valid_temp = float(f.readline())
    Valid_humi = float(f2.readline())
    f.close()
    f2.close()

    # 현재 스마트팜에 온습도를 측정해서 변수에 저장
    h, t = cel()

    # LCD 디스플레이에 현재 온습도와 현재 시간 출력
    lcd_init()
    index = 0
    while index < 5:  # 5초 동안 현재 시간 출력
        printDateTime()
        time.sleep(1)
        index += 1
    # 온습도 출력
    lcd_string("temperature:"+str(t), LCD_LINE_1)
    lcd_string("humidity:"+str(h), LCD_LINE_2)
    time.sleep(1)

    # 온도가 적정 온도보다 높으면 팬을 동작하게 함
    print("fan loading...")
    if t > Valid_temp:
        time.sleep(1)
        GPIO.output(Transitor, GPIO.HIGH)
        time.sleep(5)
    elif t <= Valid_temp:
        GPIO.output(Transitor, GPIO.LOW)

    # 습도가 적정 습도보다 낮으면 서보모터를 돌림
    if state == 0 and h < Valid_humi:  #
        servo_on()
        state = 1
    elif state == 1 and h >= Valid_humi:
        # 켜진 상태에서 2번 누르면 꺼짐
        servo_on()
        time.sleep(2)
        servo_on()
        state = 0
