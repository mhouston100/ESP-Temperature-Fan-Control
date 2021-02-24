from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import freesans20  # Font to use
import machine, onewire, ds18x20, time
from machine import Pin, PWM

#use_spi=False  # Tested with a 128*64 I2C connected SSD1306 display
#ssd = setup(use_spi)  # Instantiate display: must inherit from framebuf

ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

a = Pin(27, Pin.OUT)
b = Pin(27, Pin.OUT)
en = PWM(Pin(14))
en = PWM(Pin(14), freq=20000)

a.off()
b.off()

# Instantiate a writer for a specific font

#wri = Writer(ssd, freesans20)  # verbose = False to suppress console output
#Writer.set_textpos(ssd, 20, 0)  # In case a previous test has altered this

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
      curtemp = round(ds_sensor.read_temp(rom), 1)
      tempstring = "TMP:{}".format(curtemp)
      if curtemp < 25:
        a.off()
        en.duty(500)
      elif curtemp > 25 and curtemp <= 35:
        a.on()
        en.duty(500)
      elif curtemp > 35:
        a.on()
        en.duty(1023)
      #wri.printstring("\n\n")
      #wri.printstring(tempstring)
      print(tempstring)
      #ssd.show()
    time.sleep_ms(500)