import i2c_lcd_driver
import i2c_lcd_driver_26

LCD_DET = i2c_lcd_driver.lcd()
LCD_INFO = i2c_lcd_driver_26.lcd()

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