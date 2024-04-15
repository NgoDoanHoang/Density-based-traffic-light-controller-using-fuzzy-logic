import machine
from mfrc522 import MFRC522
import utime
import network
from umqtt.simple import MQTTClient

#declare pin for traffic_light led
GREEN_LIGHT = machine.Pin(16, machine.Pin.OUT)
YELLOW_LIGHT = machine.Pin(17, machine.Pin.OUT)
RED_LIGHT = machine.Pin(18, machine.Pin.OUT)
yellow_time = 3
green_time = None
red_time = None

#declare pin for rc522
CS_PIN = 5  # Chip select pin for RC522
SCK_PIN = 6  # SPI clock pin
MOSI_PIN = 7  # SPI MOSI pin
MISO_PIN = 4  # SPI MISO pin
tag = 432758496  # Card UID's

#declare pin for ir_sensor
ir_sensor_a1 = machine.Pin(8, machine.Pin.IN)
ir_sensor_a2 = machine.Pin(9, machine.Pin.IN)
ir_sensor_a3 = machine.Pin(10, machine.Pin.IN)
ir_sensor_a4 = machine.Pin(11, machine.Pin.IN)
ir_sensor_b1 = machine.Pin(12, machine.Pin.IN)
ir_sensor_b2 = machine.Pin(13, machine.Pin.IN)
ir_sensor_b3 = machine.Pin(14, machine.Pin.IN)
ir_sensor_b4 = machine.Pin(15, machine.Pin.IN)

#declare pin for led-7-segment
SER_PIN = machine.Pin(0, machine.Pin.OUT)  # Serial data input pin (DS pin of 74HC595)
SRCLK_PIN = machine.Pin(1, machine.Pin.OUT)  # Shift register clock pin (SH_CP pin of 74HC595)
RCLK_PIN = machine.Pin(2, machine.Pin.OUT)  # Storage register clock pin (ST_CP pin of 74HC595)
# 7-segment display segment codes for digits 0-9
segCode = [0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90]

# Flag declarations
# f_start_calculation = 0
# f_first_run = 0
# f_rfid_detected = 0
f_red_flag = 0
f_emergence = 0
density_ab = 0
f_count_var_for_testing = 0
f_count_var_for_testing_normal_run = 0

#Wifi network
wifi_ssid = "TP-LINK_0FA5"
wifi_password = "213546879"
# wifi_ssid ="K3"
# wifi_password = "hoanghoang02"

#mqtt broker config
mqtt_host = "test.mosquitto.org" 
mqtt_publish_topic = "density_ab"
# mqtt_publish_topic_2 = "emergence_vehicle_ab"
mqtt_subscribe_topic = "traffic_light_ab"
client_id = "direction_ab"
#others
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
client = MQTTClient(client_id, mqtt_host)  #Initialize MQTT client

# Connect to WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        print('Connecting to WiFi...')
        utime.sleep(1)
    print("Connected to WiFi")


# Function to check for RFID card
def emergence_rfid():
    # Check if a new card is present
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            if card == tag:
            # Check if the UID of the detected card matches the specified tag
                return True
    return False

#function to check density with ir_sensor
def check_density():
    global density_ab
    density_ab = 0
    if ir_sensor_a1.value() == 0:
        density_ab += 1
    if ir_sensor_a2.value() == 0:
        density_ab += 1
    if ir_sensor_a3.value() == 0:
        density_ab += 1
    if ir_sensor_a4.value() == 0:
        density_ab += 1
    # if ir_sensor_b1.value() == 0:
    #     density_ab += 1
    # if ir_sensor_b2.value() == 0:
    #     density_ab += 1
    # if ir_sensor_b3.value() == 0:
    #     density_ab += 1
    # if ir_sensor_b4.value() == 0:
    #     density_ab += 1
    return density_ab



# Function to shift out data for 7-segment display
def hc595_shift(dat):
    for bit in range(7, -1, -1):  # Shift out 8 bits (from MSB to LSB)
        SER_PIN.value((dat >> bit) & 1)
        SRCLK_PIN.value(1)
        SRCLK_PIN.value(0)
    RCLK_PIN.value(1)  # Latch the data
    RCLK_PIN.value(0)  # Reset the latch

def display_digit(num):
    tens_digit = num // 10
    units_digit = num % 10
    # Shift data for units digit
    hc595_shift(segCode[units_digit])
    # Shift data for tens digit
    hc595_shift(segCode[tens_digit])
    

# Function to set traffic light
def set_traffic_light(green_time, red_time):
    for i in range(green_time, -1, -1):
        GREEN_LIGHT.value(1)
        YELLOW_LIGHT.value(0)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)

    for i in range(yellow_time, -1, -1):  # Yellow time fixed at 3 seconds
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(1)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)

    for i in range(red_time, -1, -1):  
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(0)
        RED_LIGHT.value(1)
        display_digit(i)
        utime.sleep_ms(1000)

    for i in range(yellow_time, -1, -1):  # Yellow time fixed at 3 seconds
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(1)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)

def set_traffic_light_red_first(red_time, green_time):
    for i in range(red_time, -1, -1):  
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(0)
        RED_LIGHT.value(1)
        display_digit(i)
        utime.sleep_ms(1000)

    for i in range(yellow_time, -1, -1):  # Yellow time fixed at 3 seconds
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(1)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)
        
    for i in range(green_time, -1, -1):
        GREEN_LIGHT.value(1)
        YELLOW_LIGHT.value(0)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)

    for i in range(yellow_time, -1, -1):  # Yellow time fixed at 3 seconds
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(1)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)
        
def emergence_traffic_light(green_time):
    for i in range(green_time, -1, -1):
        GREEN_LIGHT.value(1)
        YELLOW_LIGHT.value(0)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)

    for i in range(yellow_time, -1, -1):  # Yellow time fixed at 3 seconds
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(1)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)
        
def emergence_traffic_light_red_first(green_time):
    for i in range(red_time, -1, -1):  
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(0)
        RED_LIGHT.value(1)
        display_digit(i)
        utime.sleep_ms(1000)

    for i in range(yellow_time, -1, -1):  # Yellow time fixed at 3 seconds
        GREEN_LIGHT.value(0)
        YELLOW_LIGHT.value(1)
        RED_LIGHT.value(0)
        display_digit(i)
        utime.sleep_ms(1000)
#End of "Function to set traffic light"
        
        
# MQTT connection
def connect(client):
    client.connect()

def publish_message(client, topic, message):
    client.publish(topic, message)
    print("\nMessage sent:", message)

def connect_and_subscribe():
    client.set_callback(callback_handler)
    client.subscribe(mqtt_subscribe_topic)

def callback_handler(topic, message):
    global green_time, red_time, f_red_flag, f_emergence
    # Decode the message from bytes to string
    message_str = message.decode('utf-8')
    
     # Remove 'e' if it's the first or second character
    if message_str.startswith('e'):
        message_str = message_str[1:].strip()  # Remove the leading 'e'
        f_emergence = 1
    elif len(message_str) > 1 and message_str[1] == 'e':
        message_str = message_str[0] + message_str[2:]  # Remove the second character ('e')
        f_emergence = 1
        
    #r - red_first
    if message_str.startswith('r'):
        f_red_flag = 1
        message_str = message_str[1:].strip()   # Remove the leading 'r' and any whitespace
#         print("remove r: red first")
    
    # Split the message into two parts using the comma as the delimiter
    green_str, red_str = message_str.split(',')
    
    # Convert the strings to integers
    green_time = int(green_str)
    red_time = int(red_str)
    
    #need to call emergence_red_first here
    if f_emergence == 1 and f_red_flag == 1:
        emergence_traffic_light_red_first(green_time)
        #reset light_time
        green_time = None
        red_time = None
    
    print("Received message on topic:", topic)
    print("Green Time:", green_time)
    print("Red Time:", red_time)


def emergence_vehicle_run():
    global density_ab, green_time, red_time, f_red_flag, f_count_var_for_testing
#     publish_message(client, mqtt_publish_topic, str(density_ab))
    publish_message(client, mqtt_publish_topic, "emergence_ab")
    
    #need tested more here - sleep so central can catch up
    utime.sleep_ms(1000)
    print("this func emergence_vehicle_run is called")
    
    # Wait for a response message for a specified duration
    wait_time = 2  # Time in seconds to wait for a response
    start_time = utime.time()
    while utime.time() - start_time < wait_time:
        client.check_msg()  # Check for incoming MQTT messages
        if green_time is not None and red_time is not None:
            # If both green_time and red_time are received, break the loop
#             f_count_var_for_testing = f_count_var_for_testing + 1
#             print("f_count_var_for_testing", f_count_var_for_testing)
            break
    # After waiting, check if both green_time and red_time are received
    if green_time is not None and red_time is not None:
        # Set traffic light based on received green_time and red_time
        if f_red_flag == 1:
            print("this is in act emergence_traffic_light_red_first")
            emergence_traffic_light_red_first(green_time)
        else:
            print("or maybe this emergence_traffic_light")
            emergence_traffic_light(green_time)
        
        #reset flag
        f_red_flag = 0
        
        #reset light_time
        green_time = None
        red_time = None
        
        
def normal_run():
    global density_ab, green_time, red_time, f_red_flag, f_emergence, f_count_var_for_testing_normal_run
    
    if f_emergence == 1:
        f_emergence = 0
#         print("want to run normal but not allowed")
#         print("f_emer2 = ", f_emergence)
    else:
        publish_message(client, mqtt_publish_topic, str(density_ab))
        
        #need tested more here - sleep so central can catch up
        #utime.sleep_ms(1000)
    #     f_count_var_for_testing_normal_run = f_count_var_for_testing_normal_run + 1
    #     print("normal run is called ", f_count_var_for_testing_normal_run)
        
        # Wait for a response message for a specified duration
        wait_time = 2  # Time in seconds to wait for a response
        start_time = utime.time()
        while utime.time() - start_time < wait_time:
            client.check_msg()  # Check for incoming MQTT messages
            if green_time is not None and red_time is not None:
                # If both green_time and red_time are received, break the loop
                break
        # After waiting, check if both green_time and red_time are received
        if green_time is not None and red_time is not None:
            # Set traffic light based on received green_time and red_time
            if f_red_flag == 1:
                set_traffic_light_red_first(green_time, red_time)
            else:
                set_traffic_light(green_time, red_time)
            #reset flag
            f_red_flag = 0
            
        #reset light_time
        green_time = None
        red_time = None
        
    #need tested more here - sleep so central can catch up
#      utime.sleep_ms(1000)
#End of "MQTT connection"
    

def main_loop():
    global density_ab
    
    connect_to_wifi()
    connect(client)
    connect_and_subscribe()
    
    while True:
        if emergence_rfid():
            emergence_vehicle_run()
        else:    
            check_density() 
            normal_run()



# Disconnect from MQTT broker
#client.disconnect()
 
# Call the main loop function
if __name__ == "__main__":
    main_loop()