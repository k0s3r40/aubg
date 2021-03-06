import bme680
import time
from stripcontroller import StripController
from be_client import SomethingWayClient
s = StripController()


creds = {"email":"kostadin@slavov.net",
          "password":"verysecure",
          }

cli = SomethingWayClient()

cli.login(creds)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)


for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))


sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Collect gas resistance burn-in values, then use the average
# of the last 50 values to set the upper limit for calculating
# gas_baseline.
start_time = time.time()
curr_time = time.time()
# Burn the sensor for 30 secs
burn_in_time = 300

burn_in_data = []

while curr_time - start_time < burn_in_time:
    curr_time = time.time()
    if sensor.get_sensor_data() and sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        burn_in_data.append(gas)
        print('Gas: {0} Ohms'.format(gas))
        time.sleep(1)

gas_baseline = sum(burn_in_data[-50:]) / 50.0

# Set the humidity baseline to 40%, an optimal indoor humidity.
hum_baseline = 40.0

# This sets the balance between humidity and gas reading in the
# calculation of air_quality_score (25:75, humidity:gas)
hum_weighting = 0.25

print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(
    gas_baseline,
    hum_baseline))

try:
    while True:
        if sensor.get_sensor_data():

            gas = sensor.data.gas_resistance
            gas_offset = gas_baseline - gas

            hum = sensor.data.humidity
            hum_offset = hum - hum_baseline

            # Calculate hum_score as the distance from the hum_baseline.
            if hum_offset > 0:
                hum_score = (100 - hum_baseline - hum_offset)
                hum_score /= (100 - hum_baseline)
                hum_score *= (hum_weighting * 100)

            else:
                hum_score = (hum_baseline + hum_offset)
                hum_score /= hum_baseline
                hum_score *= (hum_weighting * 100)

            # Calculate gas_score as the distance from the gas_baseline.
            if gas_offset > 0:
                gas_score = (gas / gas_baseline)
                gas_score *= (100 - (hum_weighting * 100))

            else:
                gas_score = 100 - (hum_weighting * 100)

            # Calculate air_quality_score.
            air_quality_score = hum_score + gas_score


            output = '{0:.2f}Ohms  {1:.2f} C,{2:.2f} hPa,{3:.2f} %RH. {4:.2f}AQ%'.format(
                gas, 
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity,
                air_quality_score
            )


            if air_quality_score >= 80:
                s.G()
            if air_quality_score < 80:
                s.BG()               
            if air_quality_score < 60:
                s.Y()
            if air_quality_score < 50:
                s.R()

            sensor_data =  {'GR': air_quality_score, # Aiq
                            'HUM': sensor.data.humidity,
                            'PSI': sensor.data.pressure,
                            'TMP': sensor.data.temperature,
                            }
            cli.store_data(sensor_data)

            print(output)
        time.sleep(1)

except KeyboardInterrupt:
    pass





