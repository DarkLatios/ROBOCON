import RPi.GPIO as GPIO
import time, sys
from bluetooth import *
GPIO.setmode(GPIO.BOARD)
pwm1=12
pwm2=16

GPIO.setup(pwm1, GPIO.OUT)
GPIO.setup(pwm2, GPIO.OUT)
p1=GPIO.PWM(pwm1, 100)
p2=GPIO.PWM(pwm2, 100)
p2.start(0)
p1.start(0)
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "Robocon Server",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print "Waiting for connection on RFCOMM channel %d" % port

client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info
mult = 0.0390625
div = 0.05208333
try:
    while True:
        #GPIO.output(br1, GPIO.HIGH)
        data2 = client_sock.recv(1024)
        print(len(data2))
        print "received [%s]" % data2
        data = long(data2)
        print(data)
        data3 = data
        i = 2
        d1 = [0,0,0]
        d2 = [0,0,0]
        print("Entering for loop d2 ")
        for i in range(2,-1,-1):
            temp = data%10
            d2[i]= temp
            data = data/10
            print("Exiting for loop d2")
        print(d2)
        print("Entering for loop d1")
        for i in range(2,-1,-1):
            temp = data%10
            d1[i] = temp
            data = data/10
            print("Exiting for loop d1")
        print(d1)
        f1 = d1[0]*100 #+ d1[1]*10 + d1[2]
        f2 = d2[0]*100 #+ d2[1]*10 + d2[2]
        if f1 < 320 and f2 < 240:
            #data = 'first quadrant'
            print("moving forward")
            print(f1)
            print(f2)
            pan = f1*mult
            tilt = f2*div
            print(pan)
            print(tilt)
            p1.ChangeDutyCycle(pan)
            p2.ChangeDutyCycle(tilt) 
        else:
            print("invalid")     
        #data = 'input invalid!'
        client_sock.send(data2)
        print "Sending Data"     
except IOError:
    pass

print "disconnected"

client_sock.close()
server_sock.close()
print "all done"
