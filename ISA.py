import ISAlib
import sys

altitude = float(input("Altitude (m): "))
        
def getLayer(altitude):
    for layer in ISAlib.layers:
        if altitude >= layer.hBase and altitude <= layer.hCeil:
            return layer
    print("out of bounds for calculation (up to 50km)")
    sys.exit()

pressure = ISAlib.calc_pressure(altitude, getLayer(altitude))
temperature = ISAlib.calc_temp(altitude, getLayer(altitude))
density = ISAlib.calc_density(pressure, temperature)

print(f"T = {temperature}")
print(f"p = {pressure}")
print(f"P = {density}")
