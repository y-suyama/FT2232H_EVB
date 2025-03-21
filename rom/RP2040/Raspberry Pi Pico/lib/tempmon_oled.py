import machine
import utime
from machine import Pin, I2C
import ssd1306
import k_thermo
import tmpADC
import tmpOFFSET
from tmpOFFSET import offset

while True:
    # RP2040温度センサの値をリード
    mcusensor_rd = machine.ADC(4)
    conv_fact = 3.3 / (65535)
    mcusensor_tmp = mcusensor_rd.read_u16() * conv_fact
    # ADC1熱電対,内蔵温度センサリード
    ch1 = tmpADC.conv(1,1,offset[0])
    ch2 = tmpADC.conv(1,2,offset[1])
    tmp1 = tmpADC.inttmp(1)
    # ADC2熱電対,内蔵温度センサリード
    ch3 = tmpADC.conv(2,3,offset[2])
    ch4 = tmpADC.conv(2,4,offset[3])
    tmp2 = tmpADC.inttmp(2)
    # OLEDに情報表示
    # using default address 0x3C
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    display.text('ADC1Tmp:{:.2f}'.format(tmp1 * 0.03125)+'deg', 0, 0, 1)
    display.text('ADC2Tmp:{:.2f}'.format(tmp2 * 0.03125)+'deg', 0, 8, 1)
    display.text('MCU_Tmp:{:.2f}'.format(27 - (mcusensor_tmp - 0.706)/0.001721)+'deg', 0, 16, 1)
    if ch1 > 1000:
        display.text('ch1_Tmp:--------', 0, 24, 1)
    else:
        display.text('ch1_Tmp:{:.2f}'.format(ch1)+'deg', 0, 24, 1)
    if ch2 > 1000:
        display.text('ch2_Tmp:--------', 0, 32, 1)
    else:
        display.text('ch2_Tmp:{:.2f}'.format(ch2)+'deg', 0, 32, 1)
    if ch3 > 1000:
        display.text('ch3_Tmp:--------', 0, 40, 1)
    else:
        display.text('ch3_Tmp:{:.2f}'.format(ch3)+'deg', 0, 40, 1)
    if ch4 > 1000:
        display.text('ch4_Tmp:--------', 0, 48, 1)
    else:
        display.text('ch4_Tmp:{:.2f}'.format(ch4)+'deg', 0, 48, 1)
    display.show()

