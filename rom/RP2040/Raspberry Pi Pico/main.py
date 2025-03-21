import machine
import utime
import time
from machine import Pin, SPI, I2C, Timer
import tmpOFFSET
# Main
# メインスレッドで実行する関数
def main():
    while True:
        with open('/lib/tempmon_oled.py', 'r') as file:
            exec(file.read())
#        print('CTRL-B to exit!!')
# main関数を呼び出して実行
if __name__ == "__main__":
    main()
