import machine, display, time, math, network, utime
from utime import sleep
from machine import Pin, I2C, SPI, PWM, ADC
import network, socket
from micropyserver import MicroPyServer
import utils
import json

tft = display.TFT()
tft.init(tft.ST7789,bgr=False,rot=tft.LANDSCAPE, miso=17,backl_pin=4,backl_on=1, mosi=19, clk=18, cs=5, dc=16)
tft.setwin(40,52,320,240)
for i in range(0,240):
  color=0xFFFFFF 
  tft.line(i,0,i,135,color)
tft.set_fg(0xFFFFFF)
tft.set_bg(0xFFFFFF)
   
ssid="Livebox-0F30"
password = ""

wifi = network.WLAN(network.STA_IF)
##ap_if = network.WLAN(network.AP_IF)
##ap_if.active(True)
wifi.active(True)
wifi.connect(ssid, password)
wifi.ifconfig(('192.168.1.32', '255.255.255.0', '192.168.1.1', '192.168.1.1'))

#import upip
#upip.install('mypackage')

#network.telnet.start(user="m",password="m")

soil1 = ADC(Pin(36))
s1 = 100
min_soil=0
max_soil=1500
soil1.atten(ADC.ATTN_11DB)
#soil1.width(ADC.WIDTH_12BIT)
soil2 = ADC(Pin(39))
s2 = 100
soil2.atten(ADC.ATTN_11DB)
#soil2.width(ADC.WIDTH_12BIT)
soil3 = ADC(Pin(32))
s3 = 100
soil3.atten(ADC.ATTN_11DB)
#soil3.width(ADC.WIDTH_12BIT)
soil4 = ADC(Pin(33))
s4 = 100
soil4.atten(ADC.ATTN_11DB)
#soil4.width(ADC.WIDTH_12BIT)

if __name__=='__main__':
    
    server = MicroPyServer()

    while(True):

        def return_json(request):
            s1 = (max_soil-soil1.read())*100/(max_soil-min_soil)
            #s1 = soil1.read()
            sval1 = '1: {:.1f} %'.format(s1)
            snum1 = '{:.1f}'.format(s1)
            s2 = (max_soil-soil2.read())*100/(max_soil-min_soil)
            sval2 = '2: {:.1f} %'.format(s2)
            snum2 = '{:.1f}'.format(s2)
            s3 = (max_soil-soil3.read())*100/(max_soil-min_soil)
            sval3 = '3: {:.1f} %'.format(s3)
            snum3 = '{:.1f}'.format(s3)
            s4 = (max_soil-soil4.read())*100/(max_soil-min_soil)
            sval4 = '4: {:.1f} %'.format(s4)
            snum4 = '{:.1f}'.format(s4)

            tft.text(20, 20, sval1, 0x000000)
            tft.text(20, 40, sval2, 0x000000)
            tft.text(20, 60, sval3, 0x000000)
            tft.text(20, 80, sval4, 0x000000)
            
            json_str = json.dumps({"par1": snum1, "par2": snum2, "par3": snum3, "par4": snum4})
            server.send("HTTP/1.0 200 OK\r\n")
            server.send("Content-Type: application/json\r\n\r\n")
            server.send(json_str)

        server.add_route("/", return_json)
        server.start()

        utime.sleep_ms(1000)
