# Density-based-traffic-light-controller-using-fuzzy-logic

This is my graduation thesis. 
More details will be updated later.

Hardware:
3 RP Pico W     (since it is required to use any microcontroller which follows ARM architecture)
16 IR_sensor    (since I was told not to do so: "With this topic, you focus on the algorithm, I will let another student focus on how to detect density with another topic")
2 RC522         (handle the case when emergence vehicles need to pass by quick)
12 LED          (3 colors)
4 LED 7-Segment (displaying numbers)
12 Resister, ... others small components

The idea is at the same time, 2 opposite direction will have the same light color and light time, so I just need 2 RP_Pico_W for that.
The central one will process data received from those 2 and fuzzificate them, then continue calculate further.
After that, it will send to node pico information about what light color is onn first and for how long.

The original system was with C, ESP32, STM32. However, I was asked to change, that is why fuzzy logic algorithm has a file written in C.  
