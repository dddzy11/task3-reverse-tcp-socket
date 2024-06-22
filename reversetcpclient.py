import socket
import random
import string
import argparse
#变量定义
Initialization=1
Agree=2
reverseRequest=3
reverseAnswer=4
bufferSize=1024 #缓冲区大小
#生成固定长度的全英文可打印字符的ASCII随机文件
def create_file(filename, filesize):
    chars=string.ascii_letters+string.digits+string.punctuation#排除空格和特殊字符
    with open(filename,'w') as file:
        for _ in range(filesize):
            c=random.choice(chars)
            file.write(c)
# 读取文件，随机确定各块的字节长度
def read_blocks(filename, Lmin, Lmax):
    with open(filename, 'r') as file:
        text=file.read()
        total_length=len(text)
        print(f"total_length: {total_length}")
        block_sizes=[]
        last_chars=total_length
        while last_chars>Lmin:#随机确定各块的字节长度，直到最后一块剩余字符长度<=Lmin
            size=random.randint(Lmin, min(Lmax,last_chars))
            block_sizes.append(size)
            last_chars-=size
        if last_chars>0:#最后一块
            block_sizes.append(last_chars)
        N=len(block_sizes)#要请求server来reverse的块数
        print(f"Block sizes: {block_sizes}")
        print(f"Total blocks: {N}")
        return text,block_sizes,N
#主函数
def main(serverIP, serverPort,fileSize,Lmin,Lmax):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((serverIP, serverPort))
        create_file('ascii_test.txt', fileSize)#生成随机ASCII文件
        text,block_sizes,N=read_blocks('ascii_test.txt',Lmin,Lmax)
        initialization_packet=(Initialization).to_bytes(2, 'big')+N.to_bytes(4, 'big')#发送Initialization报文
        client_socket.sendall(initialization_packet)
        agree_packet=client_socket.recv(bufferSize)#接收agree报文
        if int.from_bytes(agree_packet[:2],'big') != Agree:#未收到agree报文，结束
            print("not received agree packet ")
            return
        #发送reverse数据
        out_file='reversed_text.txt'
        with open(out_file,'w') as outfile:
            for i,size in enumerate(block_sizes,start=1):
                block=text[:size]#此块的文本内容
                text=text[size:]#更新剩余文本
                request_packet=(reverseRequest).to_bytes(2, 'big')+size.to_bytes(4, 'big')+block.encode()#构造本次reverseRequest报文
                client_socket.sendall(request_packet)
                #接收reversed报文
                reversed_packet=client_socket.recv(bufferSize)
                packet_type,data_length=int.from_bytes(reversed_packet[:2], 'big'), int.from_bytes(reversed_packet[2:6],'big')#解码
                if packet_type==reverseAnswer:
                    reversed_block=reversed_packet[6:6+data_length].decode()
                    print(f"第{i}块: {reversed_block}")
                    outfile.write(reversed_block+'\n')
    except Exception as e:
        print(f"error:{e}")
    finally:
        client_socket.close()
#命令行方式下，输入地址，端口，size
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="tcpclient")
    parser.add_argument('--serverIP', type=str, required=True, default='192.168.10.130',help='Server IP address')
    parser.add_argument('--serverPort', type=int, required=True, default=12345,help='Server port number')
    parser.add_argument('--fileSize', type=int, default=1000, help='Reverse Fize size')
    parser.add_argument('--Lmin', type=int, default=10, help='Minimum block size')
    parser.add_argument('--Lmax', type=int, default=150, help='Maximum block size')
    args = parser.parse_args()#解析命令行参数  

    main(args.serverIP, args.serverPort, args.fileSize, args.Lmin, args.Lmax)
