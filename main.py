import socket;
import ipaddress;

ipToDevice = {}
deviceToIp = {}




class SwitchSource:
    def __init__(self, device, switchNum):
        self.device = device
        self.switchNum = switchNum
    def __str__ (self):
        return 'SwitchSource(device=' + str(self.device) + ' ,switchNum=' + str(self.switchNum) + ')'
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        return str(self) == str(other)


class LightDest:
    def __init__(self, device, lightNum):
        self.device = device
        self.lightNum = lightNum

deviceMappings = { #9 clients 2 buttons & 7 lights
    SwitchSource(0xC0, 0xE0): [LightDest(0xC0,0), LightDest(0xC5, 0)],
    SwitchSource(0xC0, 0xF0): [LightDest(0xC1,0), LightDest(0xC6, 1)],
    SwitchSource(0xC1, 0xE0): [LightDest(0xC2,0), LightDest(0xC7, 2)],
    SwitchSource(0xC1, 0xF0): [LightDest(0xC2,0), LightDest(0xC8, 3)],
    SwitchSource(0xC2, 0xE0): [LightDest(0xC3,0), LightDest(0xC0, 4)],
    SwitchSource(0xC2, 0xF0): [LightDest(0xC3,0), LightDest(0xC1, 5)],
    SwitchSource(0xC3, 0xE0): [LightDest(0xC4,0), LightDest(0xC2, 6)],
    SwitchSource(0xC3, 0xF0): [LightDest(0xC4,0), LightDest(0xC3, 0)],
    SwitchSource(0xC4, 0xE0): [LightDest(0xC5,0), LightDest(0xC4, 1)],
    SwitchSource(0xC4, 0xF0): [LightDest(0xC5,0), LightDest(0xC5, 2)],
    SwitchSource(0xC5, 0xE0): [LightDest(0xC6,0), LightDest(0xC6, 3)],
    SwitchSource(0xC5, 0xF0): [LightDest(0xC6,0), LightDest(0xC7, 4)],
    SwitchSource(0xC6, 0xE0): [LightDest(0xC7,0), LightDest(0xC8, 5)],
    SwitchSource(0xC6, 0xF0): [LightDest(0xC7,0), LightDest(0xC0, 6)],
    SwitchSource(0xC7, 0xE0): [LightDest(0xC8,0), LightDest(0xC1, 0)],
    SwitchSource(0xC7, 0xF0): [LightDest(0xC8,0), LightDest(0xC2, 1)],
    SwitchSource(0xC8, 0xE0): [LightDest(0xC0,0), LightDest(0xC3, 2)],
    SwitchSource(0xC8, 0xF0): [LightDest(0xC0,0), LightDest(0xC4, 3)],
    SwitchSource(0xC0, 0xE1): [LightDest(0xC0,0), LightDest(0xC5, 0)],
    SwitchSource(0xC0, 0xF1): [LightDest(0xC1,0), LightDest(0xC6, 1)],
    SwitchSource(0xC1, 0xE1): [LightDest(0xC2,0), LightDest(0xC7, 2)],
    SwitchSource(0xC1, 0xF1): [LightDest(0xC2,0), LightDest(0xC8, 3)],
    SwitchSource(0xC2, 0xE1): [LightDest(0xC3,0), LightDest(0xC0, 4)],
    SwitchSource(0xC2, 0xF1): [LightDest(0xC3,0), LightDest(0xC1, 5)],
    SwitchSource(0xC3, 0xE1): [LightDest(0xC4,0), LightDest(0xC2, 6)],
    SwitchSource(0xC3, 0xF1): [LightDest(0xC4,0), LightDest(0xC3, 0)],
    SwitchSource(0xC4, 0xE1): [LightDest(0xC5,0), LightDest(0xC4, 1)],
    SwitchSource(0xC4, 0xF1): [LightDest(0xC5,0), LightDest(0xC5, 2)],
    SwitchSource(0xC5, 0xE1): [LightDest(0xC6,0), LightDest(0xC6, 3)],
    SwitchSource(0xC5, 0xF1): [LightDest(0xC6,0), LightDest(0xC7, 4)],
    SwitchSource(0xC6, 0xE1): [LightDest(0xC7,0), LightDest(0xC8, 5)],
    SwitchSource(0xC6, 0xF1): [LightDest(0xC7,0), LightDest(0xC0, 6)],
    SwitchSource(0xC7, 0xE1): [LightDest(0xC8,0), LightDest(0xC1, 0)],
    SwitchSource(0xC7, 0xF1): [LightDest(0xC8,0), LightDest(0xC2, 1)],
    SwitchSource(0xC8, 0xE1): [LightDest(0xC0,0), LightDest(0xC3, 2)],
    SwitchSource(0xC8, 0xF1): [LightDest(0xC0,0), LightDest(0xC4, 3)]
}


def main():
    print("Hello World!")
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mysocket.bind(('', 22222))
    while True:
        data, addr = mysocket.recvfrom(1024)
        if ipToDevice.get(addr) == None:
            print ("Registerring " + addr[0] + " as " + data.hex("-"))
            print(data)
            ipToDevice[addr[0]] = data
            deviceToIp[data] = addr[0]
        else:
            print('Received:' + data.decode("utf-8") + ' From: ' + addr[0] + ' Port: ' + str(addr[1]))
            addr = ipToDevice[addr[0]]
            #data = hash(data), Data = 0xE0,0xE1,0xF0,0xF1
            #addr = hash(data)
            #repeat for each light we will turn on
            mysocket.sendto(data, addr)





if __name__ == "__main__":
    main()
