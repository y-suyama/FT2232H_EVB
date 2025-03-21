#exec(open('cmd_tmpmon_oled.py').read())
#exec(open('cmd_tmpmon_term.py').read())
import machine
import utime
from machine import Pin, I2C
import tmpADC


# ADC1熱電対リード
print('ADC1 Tmp:{:.2f}'.format(tmpADC.inttmp(1))+'deg')
print('ADC2 Tmp:{:.2f}'.format(tmpADC.inttmp(2))+'deg')
print('ch1 Tmp:{:.2f}'.format(tmpADC.conv(1,1,offset[0]))+'deg')
print('ch2 Tmp:{:.2f}'.format(tmpADC.conv(1,2,offset[1]))+'deg')
# ADC2熱電対リード
print('ch3 Tmp:{:.2f}'.format(tmpADC.conv(2,3,offset[2]))+'deg')
print('ch4 Tmp:{:.2f}'.format(tmpADC.conv(2,4,offset[3]))+'deg')
