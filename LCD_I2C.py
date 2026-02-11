import utime
from machine import I2C

# Địa chỉ mặc định thường là 0x27
class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = True
        utime.sleep_ms(20)
        # Các lệnh khởi tạo LCD 1602 cơ bản
        self.hal_write_command(0x33)
        self.hal_write_command(0x32)
        self.hal_write_command(0x28)
        self.hal_write_command(0x0C)
        self.hal_write_command(0x06)
        self.hal_write_command(0x01)
        utime.sleep_ms(2)

    def hal_write_command(self, cmd):
        self.hal_write_8bits(cmd & 0xF0)
        self.hal_write_8bits((cmd << 4) & 0xF0)

    def hal_write_8bits(self, value):
        bit_bl = 0x08 if self.backlight else 0x00
        self.i2c.writeto(self.i2c_addr, bytes([value | bit_bl | 0x04]))
        self.i2c.writeto(self.i2c_addr, bytes([value | bit_bl]))

    def putstr(self, string):
        for char in string:
            self.hal_write_data(ord(char))

    def hal_write_data(self, data):
        self.hal_write_8bits((data & 0xF0) | 0x01)
        self.hal_write_8bits(((data << 4) & 0xF0) | 0x01)

    def clear(self):
        self.hal_write_command(0x01)
        utime.sleep_ms(2)

    def move_to(self, cursor_x, cursor_y):
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40
        self.hal_write_command(0x80 | addr)