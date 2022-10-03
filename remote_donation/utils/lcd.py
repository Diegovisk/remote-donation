
from remote_donation.utils.i2c_lcd_driver import lcd as LcdDet
from remote_donation.utils.i2c_lcd_driver_26 import lcd as LcdInfo

LCD_DET = LcdDet()
LCD_INFO = LcdInfo()

def print_det_lcd(msgs):
    LCD_DET.lcd_clear()
    LCD_DET.print_lcd(msgs[0])
    LCD_DET.print_lcd(msgs[1], 2)

def print_info_lcd(msgs):
    LCD_INFO.lcd_clear()
    LCD_INFO.print_lcd(msgs[0])
    LCD_INFO.print_lcd(msgs[1], 2)

def clear_info_lcd():
    LCD_INFO.lcd_clear()

def clear_det_lcd():
    LCD_DET.lcd_clear()

def det_backlight_on():
    LCD_DET.backlight(1)

def det_backlight_off():
    LCD_DET.backlight(0)

def info_backlight_on():
    LCD_INFO.backlight(1)

def info_backlight_off():
    LCD_INFO.backlight(0)