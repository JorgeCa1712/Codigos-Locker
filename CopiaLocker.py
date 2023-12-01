from machine import Pin, UART, I2C
from kb4x4 import kb4x4
from i2c_lcd import I2cLcd
import time

# Inicialización de I2C para la pantalla LCD
i2c_lcd = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
lcd = I2cLcd(i2c_lcd, 0x27, 2, 16)  # Cambia la dirección 0x27 según tu configuración

# Configuración de UART para la comunicación con el sensor de huella digital A698
uart = UART(2, tx=26, rx=25)  # Configura los pines UART según tu conexión

teclado = kb4x4()
led = Pin(13, Pin.OUT)  # Pin correcto
Led = Pin(12, Pin.OUT)  # Pin incorrecto

# Contraseña predefinida
contrasena_correcta = ['1', '2', '3']
ingresado = []

lcd.clear()
lcd.putstr("Bienvenido       Locker")
time.sleep(2)
lcd.clear()
lcd.putstr("Ingresa pin....:")

print("Bienvenido   Locker")
time.sleep(2)
print("Ingresa pin o   huella")

while True:
    # Leer la huella digital
    uart.write(b"AT\n")
    response = uart.readline()

    if response and b"OK" in response:
        lcd.clear()
        lcd.putstr("Leyendo huella...")
        print("Leyendo huella...")

        uart.write(b"AT+MATCH?\n")
        response = uart.readline()

        if response and b"OK" in response:
            lcd.clear()
            lcd.putstr("Huella correcta")
            led.on()
            Led.off()
            time.sleep(10)
            led.off()
            print("Huella correcta")
        else:
            lcd.clear()
            lcd.putstr("Huella incorrecta")
            Led.on()
            led.off()
            time.sleep(2)
            Led.off()
            print("Huella incorrecta")

        ingresado = []  # Reiniciar la lista para el nuevo intento
        lcd.clear()
        lcd.putstr("Ingresa pin o huella")
        print("Ingresa pin o huella")

    # Leer el teclado
    password = teclado.readkey()
    if password:
        if isinstance(password, tuple):
            key = password[0]
            lcd.putstr(str(key))
            print(str(key))

            if key == "D":
                if ingresado == contrasena_correcta:
                    lcd.clear()
                    lcd.putstr("Pin correcto")
                    led.on()
                    Led.off()
                    time.sleep(10)
                    led.off()
                    print("Pin correcto")
                else:
                    lcd.clear()
                    lcd.putstr("Pin incorrecto")
                    Led.on()
                    led.off()
                    time.sleep(2)
                    Led.off()
                    print("Pin incorrecto")

                ingresado = []  # Reiniciar la lista para el nuevo intento
                lcd.clear()
                lcd.putstr("Ingresa pin....:")
                print("Ingresa pin....:")

            elif len(ingresado) < len(contrasena_correcta):
                ingresado.append(key)

            if len(ingresado) == len(contrasena_correcta):
                lcd.clear()
                lcd.putstr("Pin ingresado:")
                lcd.move_to(0, 1)
                lcd.putstr("".join(map(str, ingresado)))
                print("Pin ingresado:", "".join(map(str, ingresado)))
