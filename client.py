import socket
mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Thanks to our good friends at https://www.w3schools.com/python/python_lists.asp
butt_list = [0xF, 0xE]                                                  #List of Buttons for this device
led_list = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6]                          #List of LEDs for this device


message = 0xC0                                                          #Set Client ID
mysocket.sendto(message.to_bytes(1, 'big'),('127.0.0.1',22222))         #Send Client ID
#data, addr = mysocket.recvfrom(1024)                                   #Receive and print Server Echo
#print('Received: ' + data.decode('utf-8') +
#       ' From: ' + addr[0] + ' Port: ' + str(addr[1]))
while True:                                                             #Block and wait for switch activation
    data, addr = mysocket.recvfrom(1024)
    #if data in butt_list:
    #    print('Switch ' + data + 'Pressed, activating light 0x01')
    device = data & 15
    state = (data >> 4) & 15
    if device in led_list:
        print('Led ' + device + 'In state ' + state)
    if device in butt_list:
        print('Button ' + device + 'In state ' + state)
