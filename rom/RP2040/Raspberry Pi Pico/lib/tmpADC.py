import machine
import utime
from machine import Pin, SPI
import k_thermo


def two_complement_to_signed_int(value, bit_length):
    """
    二の補数を符号付き整数に変換する関数
    
    :param value: 二の補数表現の値
    :param bit_length: ビット長
    :return: 符号付き整数に変換された値
    """
    # 二の補数を考慮して符号付き整数に変換
    if value >= 2**(bit_length - 1):
        value -= 2**bit_length
    return value

def conv(no, ch, offset):
    """
    熱電対の測定値を温度に変換する関数
    
    :param no: アクセス先の番号（1または2）
    :param ch: チャンネル番号（1から4）
    :param offset: オフセット値
    :return: 温度（℃）
    """
    txdata = bytearray(2)
    rxdata = bytearray(2)

    txdata[1] = 0x0B  # Configレジスタの設定値

    # Read Ch設定
    if ch == 1 or ch == 3:
        txdata[0] = 0x8d
    else:
        txdata[0] = 0xbd

    # SPI1初期設定
    spi = SPI(1, baudrate=4000000, polarity=0, phase=1, sck=Pin(10), mosi=Pin(11), miso=Pin(8))

    # アクセス先確認
    if no == 1:
        # SPI1_CS0_N(GPIO4)初期設定
        spi1_cs_n = Pin(4, Pin.OUT, value=1)
    else:
        # SPI1_CS1_N(GPIO24)初期設定
        spi1_cs_n = Pin(24, Pin.OUT, value=1)

    # ADS1118 Config Register Read/Write
    try:
        spi1_cs_n(0)
        utime.sleep(0.1)
        spi.write(txdata)
        utime.sleep(0.1)
    finally:
        spi1_cs_n(1)
    utime.sleep(0.1)
    try:
        spi1_cs_n(0)
        utime.sleep(0.1)
        spi.write_readinto(txdata, rxdata)
        utime.sleep(0.1)
    finally:
        spi1_cs_n(1)

    # 受信データを16ビットの整数に変換
    ret = rxdata[0] << 8
    ret += rxdata[1]

    # 二の補数を考慮して符号付き整数に変換
    ret = two_complement_to_signed_int(ret, 16)
    # Voltage変換(mV)
    ret = (ret * 0.256 * 10**3) / 2**15

    # 温度センサの温度を熱電対電圧に換算して加算
    ret += k_thermo.linear_interpolation_t_to_v(inttmp(no) * 0.03125)

    # K型熱電対の対応温度を探索
    ret = k_thermo.linear_interpolation_v_to_t(ret)
    # オフセット補正
    ret += offset
    return ret

def inttmp(no):
    """
    内部温度センサの値を取得する関数
    
    :param no: アクセス先の番号（1または2）
    :return: 内部温度センサの値
    """
    txdata = bytearray(2)
    rxdata = bytearray(2)

    txdata[1] = 0x1B  # Configレジスタの設定値
    txdata[0] = 0xBD

    # SPI1初期設定
    spi = SPI(1, baudrate=4000000, polarity=0, phase=1, sck=Pin(10), mosi=Pin(11), miso=Pin(8))

    # アクセス先確認
    if no == 1:
        # SPI1_CS0_N(GPIO4)初期設定
        spi1_cs_n = Pin(4, Pin.OUT, value=1)
    else:
        # SPI1_CS1_N(GPIO24)初期設定
        spi1_cs_n = Pin(24, Pin.OUT, value=1)

    # ADS1118 Config Register Read/Write
    try:
        spi1_cs_n(0)
        utime.sleep(0.1)
        spi.write(txdata)
        utime.sleep(0.1)
    finally:
        spi1_cs_n(1)
        utime.sleep(0.1)
    try:
        spi1_cs_n(0)
        utime.sleep(0.1)
        spi.write_readinto(txdata, rxdata)
        utime.sleep(0.1)
    finally:
        spi1_cs_n(1)

    # 受信データを14ビットの整数に変換
    ret = rxdata[0] << 6
    ret += rxdata[1] >> 2

    # 二の補数を考慮して符号付き整数に変換
    ret = two_complement_to_signed_int(ret, 14)

    return ret
