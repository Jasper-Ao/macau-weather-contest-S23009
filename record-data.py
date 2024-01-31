import serial
from weathercontest import client


client.init('w033', 'sz8ze24z')

port = 'COM3'
ser = serial.Serial(port, baudrate=4800, timeout=20)

data = {
    'LONG': 0,
    'LAT': 0,
    'PM2.5': 0,
    'PM10': 0,
    'O3': 0
}

first_line = True
try:
    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode("utf-8").rstrip()
            except UnicodeDecodeError: pass

            if first_line:
                try:
                    data['LAT'], data['LONG'] = (float(ele) for ele in line.split(','))
                    first_line = False
                except:
                    pass
                
            else:
                pm25_value, pm100_value, o3_value = [float(ele) for ele in line.split(',')]
                data['PM2.5'] = pm25_value
                data['PM10'] = pm100_value
                data['O3'] = o3_value
                client.send(data=data)
except KeyboardInterrupt:
    pass


ser.close()
