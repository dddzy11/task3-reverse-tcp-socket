import socket
#变量定义
HOST = '0.0.0.0' #监听所有可用的接口
PORT = 12345
Initialization=1
Agree=2
reverseRequest=3
reverseAnswer=4
bufferSize=1024 #缓冲区大小
#绑定地址
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("tcp server is listening")
client_socket, client_address = server_socket.accept()
print(f"connected by {client_address}")
try:
    while True:
        data=client_socket.recv(bufferSize)#接收数据
        if not data:
            break#未接收到数据，结束
        packet_type=int.from_bytes(data[:2],'big')#解码type
        if packet_type==Initialization:
            N=int.from_bytes(data[2:6],'big')#要reverse的块数
            print(f"received client initialization")
            client_socket.sendall(Agree.to_bytes(2, 'big'))#发送agree
            print(f"agree be sent")
        elif packet_type==reverseRequest:#收到reverse数据
            data_length=int.from_bytes(data[2:6], 'big')#本次Data的长度
            text=data[6:6+data_length].decode('ascii')#将字节串解码为ASCII字符串
            reversed_text=text[::-1]#reverse
            reversed_packet=(reverseAnswer).to_bytes(2,'big')+data_length.to_bytes(4,'big')+reversed_text.encode()
            client_socket.sendall(reversed_packet)
except Exception as e:
    print(f"Error: {e}")
    server_socket.close() 
# 关闭连接
client_socket.close()
server_socket.close()
