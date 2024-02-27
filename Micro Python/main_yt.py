'''
raw_set_pixel.py
This example shows how to set the pixels on the display individually without having to use pico graphics.
This method can be used to save on memory usage.
'''

import time
import network
import uasyncio as asyncio
from machine import Pin
import machine
import WIFI_CONFIG
import hub75
from network_manager import NetworkManager
import ntptime
from micropython_youtube_api import YoutubeAPI
import json
import os
from machine import I2S




WIDTH = 64
HEIGHT = 64
p1 = 40

matrix = hub75.Hub75(WIDTH, HEIGHT, panel_type=hub75.PANEL_FM6126A)

# create the rtc object
rtc = machine.RTC()

matrix.start()
matrix.clear()
try:
    from secrets import WIFI_SSID, WIFI_PASSWORD
    wifi_available = True
except ImportError:
    print("Create secrets.py with your WiFi credentials to get time from NTP")
    wifi_available = False


# Hardware definitions
led = Pin("LED", Pin.OUT, value=1)

#HEIGHT = 64
#WIDTH = 64
#MAX_PIXELS = 64

#h75 = hub75.Hub75(WIDTH, HEIGHT, stb_invert=False)

#OK
def font_0(x_pos): 
    font_logic_line(x_pos,  0x0FFC)
    font_logic_line(x_pos+1,0x0FFC)
    font_logic_line(x_pos+2,0x3033)
    font_logic_line(x_pos+3,0x3033)
    font_logic_line(x_pos+4,0x30C3)
    font_logic_line(x_pos+5,0x30C3)
    font_logic_line(x_pos+6,0x3303)
    font_logic_line(x_pos+7,0x3303)
    font_logic_line(x_pos+8,0x0FFC)
    font_logic_line(x_pos+9,0x0FFC)
#OK
def font_1(x_pos): 
    font_logic_line(x_pos,  0x0000)
    font_logic_line(x_pos+1,0x0000)
    font_logic_line(x_pos+2,0x0C03)
    font_logic_line(x_pos+3,0x0C03)
    font_logic_line(x_pos+4,0x3FFF)
    font_logic_line(x_pos+5,0x3FFF)
    font_logic_line(x_pos+6,0x0003)
    font_logic_line(x_pos+7,0x0003)
    font_logic_line(x_pos+8,0x0000)
    font_logic_line(x_pos+9,0x0000)
#OK
def font_2(x_pos): 
    font_logic_line(x_pos,  0x0C3F)
    font_logic_line(x_pos+1,0x0C3F)
    font_logic_line(x_pos+2,0x30C3)
    font_logic_line(x_pos+3,0x30C3)
    font_logic_line(x_pos+4,0x30C3)
    font_logic_line(x_pos+5,0x30C3)
    font_logic_line(x_pos+6,0x30C3)
    font_logic_line(x_pos+7,0x30C3)
    font_logic_line(x_pos+8,0x0F03)
    font_logic_line(x_pos+9,0x0F03)
#OK
def font_3(x_pos): 
    font_logic_line(x_pos,  0x300C)
    font_logic_line(x_pos+1,0x300C)
    font_logic_line(x_pos+2,0x3003)
    font_logic_line(x_pos+3,0x3003)
    font_logic_line(x_pos+4,0x30C3)
    font_logic_line(x_pos+5,0x30C3)
    font_logic_line(x_pos+6,0x33C3)
    font_logic_line(x_pos+7,0x33C3)
    font_logic_line(x_pos+8,0x3C3C)
    font_logic_line(x_pos+9,0x3C3C)
#OK
def font_4(x_pos): 
    font_logic_line(x_pos,  0x00F0)
    font_logic_line(x_pos+1,0x00F0)
    font_logic_line(x_pos+2,0x0330)
    font_logic_line(x_pos+3,0x0330)
    font_logic_line(x_pos+4,0x0C30)
    font_logic_line(x_pos+5,0x0C30)
    font_logic_line(x_pos+6,0x3FFF)
    font_logic_line(x_pos+7,0x3FFF)
    font_logic_line(x_pos+8,0x0030)
    font_logic_line(x_pos+9,0x0030)
#OK
def font_5(x_pos): 
    font_logic_line(x_pos,  0x3F0C)
    font_logic_line(x_pos+1,0x3F0C)
    font_logic_line(x_pos+2,0x3303)
    font_logic_line(x_pos+3,0x3303)
    font_logic_line(x_pos+4,0x3303)
    font_logic_line(x_pos+5,0x3303)
    font_logic_line(x_pos+6,0x3303)
    font_logic_line(x_pos+7,0x3303)
    font_logic_line(x_pos+8,0x30FC)
    font_logic_line(x_pos+9,0x30FC)
#OK
def font_6(x_pos): 
    font_logic_line(x_pos,  0x03FC)
    font_logic_line(x_pos+1,0x03FC)
    font_logic_line(x_pos+2,0x0CC3)
    font_logic_line(x_pos+3,0x0CC3)
    font_logic_line(x_pos+4,0x30C3)
    font_logic_line(x_pos+5,0x30C3)
    font_logic_line(x_pos+6,0x30C3)
    font_logic_line(x_pos+7,0x30C3)
    font_logic_line(x_pos+8,0x303C)
    font_logic_line(x_pos+9,0x303C)
#OK
def font_7(x_pos): 
    font_logic_line(x_pos,  0x3003)
    font_logic_line(x_pos+1,0x3003)
    font_logic_line(x_pos+2,0x300C)
    font_logic_line(x_pos+3,0x300C)
    font_logic_line(x_pos+4,0x3030)
    font_logic_line(x_pos+5,0x3030)
    font_logic_line(x_pos+6,0x30C0)
    font_logic_line(x_pos+7,0x30C0)
    font_logic_line(x_pos+8,0x3F00)
    font_logic_line(x_pos+9,0x3F00)
#OK   
def font_8(x_pos):
    font_logic_line(x_pos,  0x0F3C)
    font_logic_line(x_pos+1,0x0F3C)
    font_logic_line(x_pos+2,0x30C3)
    font_logic_line(x_pos+3,0x30C3)
    font_logic_line(x_pos+4,0x30C3)
    font_logic_line(x_pos+5,0x30C3)
    font_logic_line(x_pos+6,0x30C3)
    font_logic_line(x_pos+7,0x30C3)
    font_logic_line(x_pos+8,0x0F3C)
    font_logic_line(x_pos+9,0x0F3C)
#OK
def font_9(x_pos): 
    font_logic_line(x_pos,  0x0F03)
    font_logic_line(x_pos+1,0x0F03)
    font_logic_line(x_pos+2,0x30C3)
    font_logic_line(x_pos+3,0x30C3)
    font_logic_line(x_pos+4,0x30C3)
    font_logic_line(x_pos+5,0x30C3)
    font_logic_line(x_pos+6,0x30CC)
    font_logic_line(x_pos+7,0x30CC)
    font_logic_line(x_pos+8,0x0FF0)
    font_logic_line(x_pos+9,0x0FF0)

z=0

def font_logic_line(x,value):
    for y in range(0, 14):
        if value>>y & 1:
            matrix.set_pixel(x, 50-y, 90, 90, 90)
            
        else:
            matrix.set_pixel(x, 50-y, 0, 0, 0)
            



def box(x1,y1,x2,y2,color): 
    for x in range(x1, x2):
        for y in range(y1, y2):
          # bitmap[x, y] = color
            if color == 1:
                matrix.set_pixel(x, y, 90, 90, 90)
                
            if color == 2:
                matrix.set_pixel(x, y, 90, 0, 0)
                

def logic_line(x,value):
    for y in range(0, 8):
        if value>>y & 1:
            matrix.set_pixel(x, 61-y, 90, 90, 90)
            
        else:
            matrix.set_pixel(x, 61-y, 0, 0, 0)
            

# Draw even more pixels
box(19,3,45,4,2)
box(15,4,49,5,2)
box(13,5,51,6,2)
box(12,6,52,7,2)
box(11,7,53,11,2)
box(10,11,54,26,2)
box(11,26,53,30,2)
box(12,30,52,31,2)
box(13,31,51,32,2)
box(15,32,49,33,2)
box(19,33,45,34,2)

box(27,12,29,25,1)
box(29,13,31,24,1)
box(31,14,33,23,1)
box(33,15,35,22,1)
box(35,16,37,21,1)
matrix.set_pixel(37,17,100,100,100)
matrix.set_pixel(37,18,100,100,100)
matrix.set_pixel(37,19,100,100,100)
matrix.set_pixel(38,18,100,100,100)
#m
logic_line(2,0x3F) 
logic_line(3,0x20)
logic_line(4,0x38)
logic_line(5,0x20)
logic_line(6,0x1F)
#a
logic_line(8,0x16) 
logic_line(9,0x29)
logic_line(10,0x29)
logic_line(11,0x1F)
#d
logic_line(13,0x1e) 
logic_line(14,0x21)
logic_line(15,0x21)
logic_line(16,0xFF)
#e
logic_line(18,0x1e) 
logic_line(19,0x29)
logic_line(20,0x29)
logic_line(21,0x18)

#b
logic_line(24,0xFF) 
logic_line(25,0x21)
logic_line(26,0x21)
logic_line(27,0x1F)
#y
logic_line(29,0x38) 
logic_line(30,0x04)
logic_line(31,0x04)
logic_line(32,0x3F)
matrix.set_pixel(30,62,100,100,100)
matrix.set_pixel(31,62,100,100,100)

#m
logic_line(35,0x3F) 
logic_line(36,0x20)
logic_line(37,0x38)
logic_line(38,0x20)
logic_line(39,0x1F)
#o
logic_line(41,0x1e) 
logic_line(42,0x21)
logic_line(43,0x21)
logic_line(44,0x1e)
#o
logic_line(46,0x3F) 
logic_line(47,0x10)
logic_line(48,0x20)
#t
logic_line(49,0x20)
logic_line(50,0xFE)
logic_line(51,0x21)
#e
logic_line(53,0x1e) 
logic_line(54,0x29)
logic_line(55,0x29)
logic_line(56,0x18)
#n
logic_line(58,0x3F) 
logic_line(59,0x20)
logic_line(60,0x20)
logic_line(61,0x1F)


#font_1(0)
#font_0(9)
#font_0(20)
#font_0(31)
#font_0(42)
#font_0(53)

#font_5(3)
#font_6(15)
#font_7(27)
#font_8(39)
#font_9(51)

#time.sleep(5)
num = 100000
count = 0
sub_counter=3613
oldnum=100000

while num != 0:
    num //= 10
    count += 1

#print("Number of digits: " + str(count))

#x, y = rand_pixel()
#r, g, b = rand_color()
#   print('Setting Pixel x: {0} y: {1}'.format(x, y))
#
#



def get_digit(number, n):
  #  print("digits: " + str(number // 10**n % 10))
    return number // 10**n % 10

def show_digit(num,p):
    if get_digit(num, p) == 0:
        font_0(xpos)
    if get_digit(num, p) == 1:
        font_1(xpos)
    if get_digit(num, p) == 2:
        font_2(xpos)
    if get_digit(num, p) == 3:
        font_3(xpos)
    if get_digit(num, p) == 4:
        font_4(xpos)
    if get_digit(num, p) == 5:
        font_5(xpos)
    if get_digit(num, p) == 6:
        font_6(xpos)
    if get_digit(num, p) == 7:
        font_7(xpos)
    if get_digit(num, p) == 8:
        font_8(xpos)
    if get_digit(num, p) == 9:
        font_9(xpos)
print("starter1")
time.sleep(1)




def play_owlsound():
    matrix.stop()
    if os.uname().machine.count("PYBv1"):

    # ======= I2S CONFIGURATION =======
        SCK_PIN = "Y6"
        WS_PIN = "Y5"
        SD_PIN = "Y8"
        I2S_ID = 2
        BUFFER_LENGTH_IN_BYTES = 5000
    # ======= I2S CONFIGURATION =======
  
    elif os.uname().machine.count("Raspberry"):

        # ======= I2S CONFIGURATION =======
        SCK_PIN = 14
        WS_PIN = 15
        SD_PIN = 16
        I2S_ID = 0
        BUFFER_LENGTH_IN_BYTES = 5000
        # ======= I2S CONFIGURATION =======

    else:
        print("Warning: program not tested with this board")

    # ======= AUDIO CONFIGURATION =======
    #AV_FILE = "Oh No.wav"
    WAV_FILE = "free-sound-1674745346.wav"
    WAV_SAMPLE_SIZE_IN_BITS = 16
    FORMAT = I2S.STEREO
    SAMPLE_RATE_IN_HZ = 32000
    # ======= AUDIO CONFIGURATION =======

    audio_out = I2S(
        I2S_ID,
        sck=Pin(SCK_PIN),
        ws=Pin(WS_PIN),
        sd=Pin(SD_PIN),
        mode=I2S.TX,
        bits=WAV_SAMPLE_SIZE_IN_BITS,
        format=FORMAT,
        rate=SAMPLE_RATE_IN_HZ,
        ibuf=BUFFER_LENGTH_IN_BYTES,
    )

    wav = open(WAV_FILE, "rb")
    pos = wav.seek(244)  # advance to first byte of Data section in WAV file

    # allocate sample array
    # memoryview used to reduce heap allocation
    wav_samples = bytearray(1000)
    wav_samples_mv = memoryview(wav_samples)
    time.sleep(3)

    # continuously read audio samples from the WAV file
    # and write them to an I2S DAC
    print("==========  START PLAYBACK ==========")
    try:
        while True:
            num_read = wav.readinto(wav_samples_mv)
            # end of WAV file?
            if num_read == 0:
                # end-of-file, advance to first byte of Data section
                #_ = wav.seek(44)
                break
            else:
                _ = audio_out.write(wav_samples_mv[:num_read])

    except (KeyboardInterrupt, Exception) as e:
        print("caught exception {} {}".format(type(e).__name__, e))

    # cleanup
    wav.close()
    audio_out.deinit()
    print("Done")
    matrix.start()
    
def sync_time():
    if not wifi_available:
        return

    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Turn WiFi power saving off for some slow APs
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connect success or failure
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(0.2)

       # redraw_display_if_reqd()

    if max_wait > 0:
        print("Connected")

        try:
            ntptime.settime()
            print("Time set")
        except OSError:
            pass

   # wlan.disconnect()
   # wlan.active(False)

# NTP synchronizes the time to UTC, this allows you to adjust the displayed time
analog_value = machine.ADC(26)

utc_offset = 0

cnt = 0;

year, month, day, wd, hour, minute, second, _ = rtc.datetime()

last_second = second

sync_time()
# time.sleep(5)

##############################################################

# Read config
with open('config.json') as f:
    config = json.load(f)

# Create an instance of the YoutubeApi

with YoutubeAPI( config["channelid"], config["appkeyid"], config["query_interval_sec"] ) as data:
  # Read the data every X seconds
    update_interval = 61
    update_stats_time = time.time() - 10

    while True:

        if update_stats_time < time.time():
            update_stats_time = time.time() + update_interval

            print ("Subs {}".format( data.subs ) )
            print ("Views {}".format( data.views ) )
            print ("Videos {}".format( data.videos ) )

            num =  int(data.subs)
            if num>oldnum:
                print ("ny sub")
                play_owlsound()
            if num==oldnum:
                print ("ingen ny sub")
            cnt=cnt+1
            print("counter = ")
            year, month, day, wd, hour, minute, second, _ = rtc.datetime()
            print(cnt)
            print(year)
            print(month)
            print(day)
            print(wd)
            print(hour)
            print(minute)
            print(second)
            
            count = 0

            while num != 0:
                num //= 10
                count += 1
               # print("Number of digits: " + str(count))
            
            num=int(data.subs)
        
            oldnum=num
        
            box(1,37,63,51,0)
        
            if count == 1:
                xpos=27
                show_digit(num,0)
            if count == 2:
                xpos=21
                show_digit(num,1)
                xpos=33
                show_digit(num,0)
            if count == 3:
                xpos=15
                show_digit(num,2)
                xpos=27
                show_digit(num,1)
                xpos=39
                show_digit(num,0)
            if count == 4:
                xpos=9
                show_digit(num,3)
                xpos=21
                show_digit(num,2)
                xpos=33
                show_digit(num,1)  
                xpos=45
                show_digit(num,0)
            if count == 5:
                xpos=3
                show_digit(num,4)
                xpos=15
                show_digit(num,3)
                xpos=27
                show_digit(num,2)
                xpos=39
                show_digit(num,1)  
                xpos=51
                show_digit(num,0)
            if count == 6:
                xpos=-1
                show_digit(num,5)
                xpos=9
                show_digit(num,4)
                xpos=20
                show_digit(num,3)
                xpos=31
                show_digit(num,2)
                xpos=42
                show_digit(num,1)  
                xpos=53
                show_digit(num,0)
        
        matrix.set_pixel(0,63,0,100,0)
         
        time.sleep(0.2)
        matrix.set_pixel(0,63,0,0,0)
         
        time.sleep(0.2)

        potentiometer = analog_value.read_u16() >> 4
      #  print(potentiometer.read_u16())
        conversion_factor = 3.3/(4096)
      #  print("{:.2f}".format(potentiometer * conversion_factor)) 
 
        if (potentiometer * conversion_factor) > 0.3:
            p1=50
        else:
            p1=0