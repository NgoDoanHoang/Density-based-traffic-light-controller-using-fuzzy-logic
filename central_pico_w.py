import utime
import network
import math
from umqtt.simple import MQTTClient
from fuzzy_func import *

# WiFi configuration
# wifi_ssid = "K3"
# wifi_password = "hoanghoang02"
wifi_ssid = "TP-LINK_0FA5"
wifi_password = "213546879"

# MQTT broker configuration
mqtt_host = "test.mosquitto.org"
client_id = "central_pico_w"

mqtt_subscribe_topic = "density_ab"
mqtt_subscribe_topic_2 = "density_cd"
mqtt_publish_topic = "traffic_light_ab"
mqtt_publish_topic_2 = "traffic_light_cd"

# Initialize MQTT client
client = MQTTClient(client_id, mqtt_host)

#others
f_emergence_ab = 0
f_emergence_cd = 0
density_ab = None
density_cd = None
traffic_light_ab = 0
traffic_light_cd = 0
traffic_light_message_green_first = None
traffic_light_message_red_first = None

# Connect to WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        print('Connecting to WiFi...')
        utime.sleep_ms(1000)
    print("Connected to WiFi")
    

# MQTT connection and subscription
def connect(client):
    client.connect()
    
def connect_and_subscribe():
    #client.connect()
    client.set_callback(callback_handler)
    client.subscribe(mqtt_subscribe_topic)
    client.subscribe(mqtt_subscribe_topic_2)

def callback_handler(topic, message):
    global f_emergence_ab, f_emergence_cd, traffic_light_ab, traffic_light_cd, density_ab, density_cd, traffic_light_message_green_first, traffic_light_message_red_first
    
    message = message.decode('utf-8')
    print("Received message on topic:", topic)
    print("Message:", message)
    
    if message == "emergence_ab":
        f_emergence_ab = 1
        print("look here - current density_ab = ", density_ab)
        print("value after raise flag - current density_cd = ", density_cd)
#         density_ab = None
#         density_cd = None
    elif message == "emergence_cd":
        f_emergence_cd = 1
        print("look here 2 - current density_ab = ", density_ab)
        print("value after raise flag- current density_cd = ", density_cd)
#         density_ab = None
#         density_cd = None
        
# Check if both types of messages have been received
    if f_emergence_ab == 1 and f_emergence_cd == 1:       
        client.publish(mqtt_publish_topic, f"re{15},{15}")
        client.publish(mqtt_publish_topic_2, f"re{15},{15}")
#         density_ab = None
#         density_cd = None
    elif f_emergence_ab == 1:
#         density_ab = None
#         density_cd = None
#         utime.sleep_ms(500)   #test here 
        client.publish(mqtt_publish_topic_2, f"re{10},{10}")
        client.publish(mqtt_publish_topic, f"e{10},{10}")
        #test
#         utime.sleep_ms(1000)
#         client.publish(mqtt_publish_topic_2, f"re{10},{10}")
        print("handle f_emer_ab case=1 - sent here\n")
        density_ab = None
        density_cd = None
    elif f_emergence_cd == 1:
        client.publish(mqtt_publish_topic, f"re{5},{5}")
        client.publish(mqtt_publish_topic_2, f"e{5},{5}")
        density_ab = None
        density_cd = None
    
    f_emergence_ab = 0
    f_emergence_cd = 0
    
#normal case
    if topic == b'density_ab' and message != "emergence_ab":
        density_ab = int(message)
        #print("this is density ab", density_ab)
    elif topic == b'density_cd' and message != "emergence_cd":
        density_cd = int(message)
        #print("this is density cd", density_cd)
        
    if density_ab is not None and density_cd is not None and message != "emergence_ab" and message != "emergence_ab":
#         traffic_light_ab, traffic_light_cd = fuzzy_logic_algorithm(density_ab, density_cd)
        traffic_light_ab = 2
        traffic_light_cd = 2
        
        print("this is result to send back:", traffic_light_ab, traffic_light_cd, "\n")
        
         # Concatenate traffic_light_ab and traffic_light_cd into a single string
        traffic_light_message_green_first = f"{traffic_light_ab},{traffic_light_cd}"
        traffic_light_message_red_first = f"r{traffic_light_ab},{traffic_light_cd}"
        client.publish(mqtt_publish_topic, traffic_light_message_green_first)
        client.publish(mqtt_publish_topic_2, traffic_light_message_red_first)
        
        print("this is density ab cd after sent normal case:", density_ab, density_cd)
        
        #reset
        traffic_light_ab = 0
        traffic_light_cd = 0
        traffic_light_message_green_first = None
        traffic_light_message_red_first = None
        density_ab = None
        density_cd = None

# Main loop
def main_loop():
    connect_to_wifi()
    connect(client)
    connect_and_subscribe()
    
    while True:
        client.check_msg()
        

# Call the main loop function
if __name__ == "__main__":
    main_loop()

