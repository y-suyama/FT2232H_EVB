import machine
import utime
from machine import Pin, SPI, I2C

# boot rp2040
# CPU周波数を133MHzに設定
new_freq = 133000000 # 133MHz
machine.freq(new_freq)
current_freq = machine.freq()
# ADC0をInput, Pull up, IRQ待ちに設定
adc0_pin = Pin(0, Pin.IN, Pin.PULL_UP)
def adc0_irq_handler(pin):
    print("割り込み発生 - ピン状態:", pin.value())
# FALLING エッジ（HIGH から LOW への変化）で割り込みを発生
adc0_pin.irq(trigger=Pin.IRQ_FALLING, handler=adc0_irq_handler)
# RP2040温度センサの値をリード
#mcusensor_rd = machine.ADC(4)
#conv_fact = 3.3 / (65535)
#mcusensor_tmp = mcusensor_rd.read_u16() * conv_fact



