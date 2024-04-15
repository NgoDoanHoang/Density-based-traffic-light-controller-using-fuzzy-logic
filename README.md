# Density-based-traffic-light-controller-using-fuzzy-logic

This is my graduation thesis. <br />
More details will be updated later.<br />

Hardware:<br />
3 RP Pico W     (since it is required to use any microcontroller which follows ARM architecture)<br />
16 IR_sensor    (since I was told not to do so: "With this topic, you focus on the algorithm, I will let another student focus on how to detect density with another topic")<br />
2 RC522         (handle the case when emergence vehicles need to pass by quick)<br />
12 LED          (3 colors)<br />
4 LED 7-Segment (displaying numbers)<br />
12 Resister, ... others small components<br />

Software:<br />
Thonny_IDE <br />
umqtt_Library <br />

How it works:<br />
The idea is at the same time, 2 opposite direction will have the same light color and light time, so I just need 2 RP_Pico_W for that.<br />
The central one will process data received from those 2 and fuzzificate them, then continue calculate further.<br />
After that, it will send to node pico information about what light color is onn first and for how long.<br />

The original system was with C, ESP32, STM32. However, I was asked to change, that is why fuzzy logic algorithm has a file written in C.  <br />
