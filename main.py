import io
import os
import socket
import struct
import time
import picamera
import sys
from Ultrasonic import Ultrasonic
from servo import Servo
from Motor import Motor
from Buzzer import Buzzer
from Led import Led, Color

led = Led()
buzzer = Buzzer()
pwm = Servo()
ultrasonic = Ultrasonic()
motor = Motor()
MIDDLE_ANGLE = 90
DELTA = 35
DATA_PTS = 2
SPEED = 900
TURNING_SPEED = 1500

def setMotor(distances, counter):
    # if min(distances) < 15:
    #     motor.setMotorModel(0, 0, 0, 0)
    #     buzzer.run('1')
    #     return
    left = distances[:DATA_PTS]
    right = distances[-DATA_PTS:][::-1]
    if min(distances) < 30:
        buzzer.run('1')
        led.colorWipe(led.strip, Color(255,255,0))  #yellow
        if min(left) < min(right):
            motor.setMotorModel(TURNING_SPEED, TURNING_SPEED, -TURNING_SPEED, -TURNING_SPEED)
        else:
            motor.setMotorModel(-TURNING_SPEED, -TURNING_SPEED, TURNING_SPEED, TURNING_SPEED)
        time.sleep(0.15)
        led.colorWipe(led.strip, Color(255,0,0))  #red
        motor.setMotorModel(0, 0, 0, 0)
    else:
        buzzer.run('0')
        led.colorWipe(led.strip, Color(0,255,0))  #green
        motor.setMotorModel(SPEED, SPEED, SPEED, SPEED)
        # if counter % 2 == 0:
        #     motor.setMotorModel(SPEED, SPEED, SPEED, SPEED)
        # else:
        #     motor.setMotorModel(0, 0, 0, 0)

def setMotorTest(a, b):
    motor.setMotorModel(0, 0, 0, 0)

def run(counter):
    distances = []
    for angle in range(MIDDLE_ANGLE-DELTA*DATA_PTS, MIDDLE_ANGLE+DELTA*DATA_PTS+1, DELTA):
        pwm.setServoPwm('0', angle) # horizontal
        time.sleep(0.1)
        data=ultrasonic.get_distance()   #Get the value
        distances.append(data)
    print("Distances: ", distances)
    setMotor(distances, counter)

# Initialize camera and ultrasonic sensor loocation
def reset():
    pwm.setServoPwm('0', MIDDLE_ANGLE) # horizontal
    pwm.setServoPwm('1', 125) # vertical
    motor.setMotorModel(0, 0, 0, 0)
    buzzer.run('0')
    led.colorWipe(led.strip, Color(0,0,0))  #turn off the light

if __name__ == '__main__':
    reset()
    for i in range(60):
        run(i)
    reset()
