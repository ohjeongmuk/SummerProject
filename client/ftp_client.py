import os
os.chdir('myfiles')

import socket
from time import sleep
from threading import Thread
import asyncio

IP, DPORT = 'localhost', 8085

def to_hex(number):
    # Verify our assumption: error is printed and program exists if assumption is violated
    assert number <= 0xffffffff, "Number too large"
    return "{:08x}".format(number)

async def recv_intro_message(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()

async def recv_message(reader: asyncio.StreamReader):
    full_data = await reader.readline()
    return full_data.decode()


async def send_long_message(writer: asyncio.StreamWriter, data):
    await asyncio.sleep(1)

    writer.write(to_hex(len(data)).encode())
    writer.write(data.encode())

    await writer.drain()

async def connect():
    reader, writer = await asyncio.open_connection(IP, DPORT)    

    # TODO: introduction message here
    for i in range(0, 8):
        message = await recv_intro_message(reader)
        print(message)

    while(1):
        user_input = input("To server: ")
        file_name = user_input.split(" ")
        if file_name[0] == "put" and os.path.exists(file_name[1]) == False:
            print("NAK: File Doesn't Exist in Client")
            continue

        # Send message
        await send_long_message(writer, user_input)
        # receive message
        message = await recv_message(reader)
        user_input = user_input.split(" ")
        # File DownLoad
        if message == "create\n":
            print('File Downloading...')
            length = await recv_message(reader)
            length = int(length)
            with open(user_input[1], "w") as f:
                for i in range(0, length):
                    file_content = await recv_message(reader)
                    f.write(file_content)
    
        # File Upload
        elif message == "upload\n":
            print("File Uploading...")
            # 파일 오픈..
            length = 0
            with open(user_input[1], "r") as f:
                length = len(f.readlines())
                await send_long_message(writer, str(length)+'\n')
            with open(user_input[1], 'r') as f:
                await send_long_message(writer, f.read())
        elif message == "remove\n":
            print("File Remove Successful!")
        # Check file list
        elif message == "ACK\n":
            message = await recv_message(reader)
            print(message)
            continue

        # Error
        else:
            print(message)
            if user_input[0] == "close":
                break
            continue
    return 0

async def main():
    '''
        TODO: Asynchronous func and thread will be used to set up all server and client 
    '''
    tasks = []
    tasks.append(connect())
    await asyncio.gather(*tasks)
    print("done")

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())