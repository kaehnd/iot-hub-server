from distutils.log import warn
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
    SwitchSource(0xC0, 0): [LightDest(0xC0,0), LightDest(0xC5, 0)],
    SwitchSource(0xC0, 1): [LightDest(0xC1,0), LightDest(0xC6, 1)],
    SwitchSource(0xC1, 0): [LightDest(0xC2,0), LightDest(0xC7, 2)],
    SwitchSource(0xC1, 1): [LightDest(0xC2,0), LightDest(0xC8, 3)],
    SwitchSource(0xC2, 0): [LightDest(0xC3,0), LightDest(0xC0, 4)],
    SwitchSource(0xC2, 1): [LightDest(0xC3,0), LightDest(0xC1, 5)],
    SwitchSource(0xC3, 0): [LightDest(0xC4,0), LightDest(0xC2, 6)],
    SwitchSource(0xC3, 1): [LightDest(0xC4,0), LightDest(0xC3, 0)],
    SwitchSource(0xC4, 0): [LightDest(0xC5,0), LightDest(0xC4, 1)],
    SwitchSource(0xC4, 1): [LightDest(0xC5,0), LightDest(0xC5, 2)],
    SwitchSource(0xC5, 0): [LightDest(0xC6,0), LightDest(0xC6, 3)],
    SwitchSource(0xC5, 1): [LightDest(0xC6,0), LightDest(0xC7, 4)],
    SwitchSource(0xC6, 0): [LightDest(0xC7,0), LightDest(0xC8, 5)],
    SwitchSource(0xC6, 1): [LightDest(0xC7,0), LightDest(0xC0, 6)],
    SwitchSource(0xC7, 0): [LightDest(0xC8,0), LightDest(0xC1, 0)],
    SwitchSource(0xC7, 1): [LightDest(0xC8,0), LightDest(0xC2, 1)],
    SwitchSource(0xC8, 0): [LightDest(0xC0,0), LightDest(0xC3, 2)],
    SwitchSource(0xC8, 1): [LightDest(0xC0,0), LightDest(0xC4, 3)],
    SwitchSource(0xC0, 0): [LightDest(0xC0,0), LightDest(0xC5, 0)],
    SwitchSource(0xC0, 1): [LightDest(0xC1,0), LightDest(0xC6, 1)],
    SwitchSource(0xC1, 0): [LightDest(0xC2,0), LightDest(0xC7, 2)],
    SwitchSource(0xC1, 1): [LightDest(0xC2,0), LightDest(0xC8, 3)],
    SwitchSource(0xC2, 0): [LightDest(0xC3,0), LightDest(0xC0, 4)],
    SwitchSource(0xC2, 1): [LightDest(0xC3,0), LightDest(0xC1, 5)],
    SwitchSource(0xC3, 0): [LightDest(0xC4,0), LightDest(0xC2, 6)],
    SwitchSource(0xC3, 1): [LightDest(0xC4,0), LightDest(0xC3, 0)],
    SwitchSource(0xC4, 0): [LightDest(0xC5,0), LightDest(0xC4, 1)],
    SwitchSource(0xC4, 1): [LightDest(0xC5,0), LightDest(0xC5, 2)],
    SwitchSource(0xC5, 0): [LightDest(0xC6,0), LightDest(0xC6, 3)],
    SwitchSource(0xC5, 1): [LightDest(0xC6,0), LightDest(0xC7, 4)],
    SwitchSource(0xC6, 0): [LightDest(0xC7,0), LightDest(0xC8, 5)],
    SwitchSource(0xC6, 1): [LightDest(0xC7,0), LightDest(0xC0, 6)],
    SwitchSource(0xC7, 0): [LightDest(0xC8,0), LightDest(0xC1, 0)],
    SwitchSource(0xC7, 1): [LightDest(0xC8,0), LightDest(0xC2, 1)],
    SwitchSource(0xC8, 0): [LightDest(0xC0,0), LightDest(0xC3, 2)],
    SwitchSource(0xC8, 1): [LightDest(0xC0,0), LightDest(0xC4, 3)]
}


def main():
    print("Hello World!")
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mysocket.bind(('', 22222))
    while True:
        data, addr = mysocket.recvfrom(1024)
        if ipToDevice.get(addr[0]) == None:
            print ("Registerring " + addr[0] + " as " + data.hex("-"))
            ipToDevice[addr[0]] = data[0]
            deviceToIp[data[0]] = addr[0]
        else:
            devSrc = ipToDevice[addr[0]]
            switchNum = (data[0] & 0xF0) >> 4
            state = data[0] & 0x0F

            print("Client " + hex(devSrc) + ", switch: " + str(switchNum) + " changed state to: " + str(state))

            mappings = deviceMappings.get(SwitchSource(devSrc, switchNum))

            if mappings == None:
                warn("Source of device: " + hex(devSrc) + " switch: " + str(switchNum) + " has no configured mappings")

            else:
                for lightDest in mappings:
                    print("Sending state message to device: " + hex(lightDest.device) + " light: " + str(lightDest.lightNum))

                    destIp = deviceToIp.get(lightDest.device)

                    if destIp == None:
                        warn ("Device " + hex(lightDest.device) + " has not registered with the server yet.")
                    else:
                        byteToSend = (lightDest.lightNum << 4) | state

                        print("Sending message: " + hex(byteToSend) + " to IP: " + destIp)
                        mysocket.sendto(byteToSend.to_bytes(1, 'big'), (destIp, 55555)) #TODO change to 22222





if __name__ == "__main__":
    main()
