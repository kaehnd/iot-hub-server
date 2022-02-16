import socket




def main():

  mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  while True:
    messageStr = input("\nByte to send: ")
    message = int(messageStr, 16)
    mysocket.sendto(message.to_bytes(1, 'big'),('127.0.0.1',22222)) # send



if __name__ == "__main__":
    main()
