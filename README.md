# Embedded-Systems
Embedded systems lab1-lab8, midterm, final



## Lab1 LED Blinking
Blinking with an externally added LED
####影片連結 : https://youtu.be/m-hYYT4rsW4



## Lab2 LED+DH11+SR04
1. Blinking an LED if the distance received from SR04 is lower than a given threshold
2. Blinking an LED if the temperature and/or humidity from DHT11 are higher than a given threshold.
影片連結1 : https://youtu.be/Z8qd6PwdnrY 
影片連結2 : https://youtu.be/r5xhr5hkEHw



## Lab3 Bluetooth Connection
1. Connect Arduino and a mobile handset (Android or Iphone) via HC05, BT05, or HM-10 to transfer characters and show your name and student ID on the screen of the PC monitor or the mobile handset.
2. Connect two Arduinos via HC05s with one configured as the master and the other as a slave to transfer characters between them. Show the transmitted characters on the screen of each other.
影片連結1 : https://youtu.be/krotSyqFjdw
影片連結2 : https://youtu.be/uhDsLa944yg



## Lab4 Arduino Robot Car Assembling
1. Assemble the chassis kits, Arduino UNO, L298N, batteries, etc.
2. Design and implement an Arduino sketch to test the basic car control operations including forwarding, r-turn, l-turn, stop, backward, speed up, slow down, etc.
影片連結 : https://youtu.be/1aa8Fsbmbg8



## Lab5 ROS2 Node Programming
1. Write an node program to detect the temperature and humidity and print out the values periodically
2. Write two node programs: the first one is  to detect the temperature and humidity and publish a topic named "DH11TH" and the second is to subscribe the topic and print out the values periodically
影片連結1 : https://youtu.be/ma9hFZ_YAbc
影片連結2 : https://youtu.be/OenUToK7JrQ



## Lab6 Integrating ROS 2 with RPi4/Arduino Using UART
1. Establish serial communication between Raspberry Pi 4 and Arduino using PySerial and a custom bridge program
2. Develop a ROS 2 bridge on Raspberry Pi 4 that reads and parses UART data transmitted from an Arduino
影片連結 : https://youtu.be/8NxLMhevp5Y



## Lab7 Object Detection with Ultralytics YOLO and ROS 2 on RPI4
Implement ROS 2 nodes on Raspberry Pi 4 where one node captures images from a connected camera, and another performs object detection using a pretrained YOLOv8 model. The detection node periodically processes image frames and displays or publishes the detected object information.
影片連結 : https://youtu.be/EgXkmtYmbaE



## Lab8 Image Object Detection
1. Install  an camera and tensorflow lite on RPi 3.
2. Write an program to detect a specified objtect (like eye, face, hand, or so) and run on RPi3
影片連結 : https://youtu.be/6Ins6zTYk9g



## Mideterm
1. Car Tracking
The car should move from the starting line, along the  track line, to the finish line. Also, the score depends on the time to complete a lap.



2. Bluetooth Remote Control
The student should remotely control the car to move from the starting line, along the  track line, to the finish line by using a mobile phone. Similarly,  the score depends on the time to complete a lap. 
影片連結1 : https://youtube.com/shorts/5nMPmd6mDs8
影片連結2 : https://youtube.com/shorts/5nMPmd6mDs8



## Final
BalloonPopBot 
Build your smart car using Arduino, Raspberry Pi (or other embedded platforms like Jetson Nano), and integrate a camera along with sensors such as the HC-SR04 ultrasonic sensor. Design your control system in Python or C++ to guide the car in popping balloons while simultaneously avoiding collisions with walls or other cars.
影片連結 : https://youtu.be/QvDv_Z9yFdo
