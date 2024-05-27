#!/usr/bin/env python3
import board
import neopixel
import time
import math
import motoron
import pygame

tire_r=0.035 #タイヤ半径
vL = 0 #左車輪　速度
vR = 0 #右車輪　速度
vL_pre = 0 #左車輪　速度
vR_pre = 0 #右車輪　速度
vMax = 600 #速度上限
joyweight = 75 #コントローラー入力の重み

pixels=neopixel.NeoPixel(board.D18,12)

# ジョイスティックの初期化
pygame.joystick.init()
# pygameの初期化
pygame.init()
try:  # 例外が発生するかもしれないが、実行したい処理
    # ジョイスティックインスタンスの生成
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print('ジョイスティックの名前:', joy.get_name())
    print('ボタン数 :', joy.get_numbuttons())
except pygame.error:  # 例外発生時に行う処理
    print('ジョイスティックが接続されていません')


mc = motoron.MotoronI2C()

# Reset the controller to its default settings, then disable CRC.  The bytes for
# each of these commands are shown here in case you want to implement them on
# your own without using the library.
mc.reinitialize()  # Bytes: 0x96 0x74
mc.disable_crc()   # Bytes: 0x8B 0x04 0x7B 0x43

# Clear the reset flag, which is set after the controller reinitializes and counts as an error.
mc.clear_reset_flag()  # Bytes: 0xA9 0x00 0x04

# By default, the Motoron is configured to stop the motors if it does not get
# a motor control command for 1500 ms.  You can uncomment a line below to
# adjust this time or disable the timeout feature.
# mc.set_command_timeout_milliseconds(1000)
# mc.disable_command_timeout()

# Configure motor 1
mc.set_max_acceleration(1, 140)
mc.set_max_deceleration(1, 100)

# Configure motor 2
mc.set_max_acceleration(2, 140)
mc.set_max_deceleration(2, 100)



try:  #例外が発生するかもしれないが、実行したい処理
    while True:
        pygame.event.pump()
        
        if (joy.get_axis(5) > 0):
            print("press B")
            pixels[0] = (255,255,0)
            pixels[1] = (255,255,0)
            pixels[2] = (255,255,0)
            pixels[3] = (0,0,255)
            pixels[4] = (0,0,255)
            pixels[5] = (0,0,255)
            pixels[6] = (0,0,255)
            pixels[7] = (0,0,255)
            pixels[8] = (0,0,255)
            pixels[9] = (255,255,0)
            pixels[10] = (255,255,0)
            pixels[11] = (255,255,0)
            pixels.show()
        
        if (joy.get_axis(2) > 0):
            print("press X")
            pixels[0] = (255,0,0)
            pixels[1] = (255,0,0)
            pixels[2] = (255,0,0)
            pixels[3] = (0,255,0)
            pixels[4] = (0,255,0)
            pixels[5] = (0,255,0)
            pixels[6] = (0,255,0)
            pixels[7] = (0,255,0)
            pixels[8] = (0,255,0)
            pixels[9] = (255,0,0)
            pixels[10] = (255,0,0)
            pixels[11] = (255,0,0)
            pixels.show()
        
        if (joy.get_button(3) == 1):
            print("press Y")
            pixels.fill((0,0,0))
            pixels.show()
            
        if (joy.get_button(0) == 1):
            print("press A")
            pixels.fill((190,0,255))
            pixels.show()
        
        vL_pre = vL
        vR_pre = vR
        # ジョイスティックの入力
        #print('0:', joy.get_axis(0),'   1:', joy.get_axis(1),'   2:', joy.get_axis(2),'   3:', joy.get_axis(3),'   4:', joy.get_axis(4)+1,'   5:', joy.get_axis(5)+1,)
        
        if(abs(joy.get_axis(1))<0.05): #abs 絶対値
            speed=0  # コントローラのブレ入力を無効化
        else: 
            speed = (-joy.get_axis(1)) * 6 * joyweight #3.5 / tire_r
        
        if(abs(joy.get_axis(0))<0.05):
            steer=0
        #elif(joy.get_axis(0)>0.006): #elif 条件式 1 が False、条件式 2 が True のときに行う処理
            #steer =-(math.acos(joy.get_axis(0))/math.pi-0.5) * 4
            #steer = -joy.get_axis(0) * 4 * joyweight
            
        #else: # すべての条件式が False のときに行う処理
            #steer =-(math.acos(joy.get_axis(0))/math.pi-0.5) * 4
            #steer = joy.get_axis(0) * 4 * joyweight    
        
        
        trigger = -(-(joy.get_axis(2)+1) * 3 + (joy.get_axis(5)+1) * 3) * joyweight

        if(joy.get_button(4) == 1):
            joyweight = joyweight - 0.05

        if(joy.get_button(5) == 1):
            joyweight = joyweight + 0.05
        
        print("joyweight=",joyweight)
        print('speed=', speed,'steer=', steer,'trigger=', trigger)
        #tp_steer=joy.get_axis(0)*(0.003)

        # if(str(joy.get.button(1)) == 1):
        #     translation=1
        
        # if(str(joy.get.button(4)) == 1)or(joy.get.button(7)) == 1):
        #     translation=0
        
        
        # if(translation==1):
        #     vR=0.37/tire_r-t_steer
        #     vL=0.37/tire_r+t_steer
            
        # else
        if(speed > 0):
            vL=speed+steer+trigger
            vR=speed-steer-trigger
        elif(speed == 0):
            vL=trigger * 0.8
            vR=-trigger * 0.8
        elif(speed < 0):
            vL=speed-steer-trigger
            vR=speed+steer+trigger
        
        if(abs(vL)>vMax):
            if(vL>0):
                vL=vMax
            elif(vL<0):
                vL=-vMax
        if(abs(vR)>vMax):
            if(vR>0):
                vR=vMax
            elif(vR<0):
                vR=-vMax           
        
        #pygame.event.pump()

        print('vL=',vL,'    vR=',vR)

        mc.set_speed(1, int(-vL))
        mc.set_speed(2, int(vR))

        time.sleep(0.005)

except (KeyboardInterrupt, pygame.error):  #例外発生時に行う処理
    pass   #例外発生後に何も処理を行わない場合


