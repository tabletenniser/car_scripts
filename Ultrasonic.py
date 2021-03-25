import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685
class Ultrasonic:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
        self.sample_counts = 7
        self.echo_timeout_max_iter = 10000

    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin,True)
        time.sleep(0.00015)
        # time.sleep(0.000015)
        GPIO.output(self.trigger_pin,False)

    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count>0:
            count = count-1
        return count == 0

    def get_distance(self):
        distance_cm=[]
        for i in range(self.sample_counts):
            self.send_trigger_pulse()
            # assert (not self.wait_for_echo(True, self.echo_timeout_max_iter))
            self.wait_for_echo(True, self.echo_timeout_max_iter)
            start = time.time()
            echo_timed_out = self.wait_for_echo(False, self.echo_timeout_max_iter)
            distance = int((time.time()-start)/0.000058) if not echo_timed_out else 500
            distance_cm.append(distance)
        distance_cm=sorted(distance_cm)
        # print(distance_cm)
        res = distance_cm[len(distance_cm)//2]
        return int(res)

    def run_motor(self,L,M,R):
        print(L, M, R)
        if (L < 30 and M < 30 and R <30) or M < 30 :
            self.PWM.setMotorModel(-1450,-1450,-1450,-1450)
            time.sleep(0.1)
            if L < R:
                self.PWM.setMotorModel(1450,1450,-1450,-1450)
            else :
                self.PWM.setMotorModel(-1450,-1450,1450,1450)
        elif L < 30 and M < 30:
            PWM.setMotorModel(1500,1500,-1500,-1500)
        elif R < 30 and M < 30:
            PWM.setMotorModel(-1500,-1500,1500,1500)
        elif L < 20 :
            PWM.setMotorModel(2000,2000,-500,-500)
            if L < 10 :
                PWM.setMotorModel(1500,1500,-1000,-1000)
        elif R < 20 :
            PWM.setMotorModel(-500,-500,2000,2000)
            if R < 10 :
                PWM.setMotorModel(-1500,-1500,1500,1500)
        else :
            self.PWM.setMotorModel(600,600,600,600)

    def run(self):
        self.PWM=Motor()
        self.pwm_S=Servo()
        for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
        while True:
            for i in range(90,30,-60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)
            for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                self.run_motor(L,M,R)

ultrasonic=Ultrasonic()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)
