import os
os.chdir('myfiles')

import socket
import asyncio

INTERFACE, SPORT = 'localhost', 8085
CHUNK = 100

# TODO: Implement me for Part 1!
async def send_intro_message(writer):
    intro_message = "Hello! Welcome to JM's server!\n"
    writer.write(intro_message.encode())
    await writer.drain()

async def send_bash_intro(writer):
    intro_message = "----------Here is our command items you can use----------\n"
    command1 = "1. list: Check the list of files present on the server\n"
    command2 = "2. upload: Upload specific files that exist in myfiles to server files\n"
    command3 = "3. download: Download a specific file that exists in server files to myfiles\n"
    command4 = "4. remove: Delete a specific file that exists in myfiles\n"
    command5 = "5. close: Close the server.\n"
    example = "(example) list | upload filename | download filename | remove filename | close\n"
    combined_string = intro_message + command1 + command2 + command3 + command4 + command5 + example
    writer.write(combined_string.encode())
    await writer.drain()


async def send_message(writer, data):
    if type(data) == list:
        li = " ".join(data)
        li = li + "\n"
        writer.write(li.encode())
        await writer.drain()
    if type(data) == str:
        writer.write(data.encode())
        await writer.drain()

async def send_file_content(writer, data):
    writer.write(data.encode())
    await writer.drain()

    return

async def receive_long_message(reader: asyncio.StreamReader):
    data_length_hex = await reader.readexactly(8)
    # hex -> int
    data_length = int(data_length_hex, 16)
    full_data = await reader.readexactly(data_length)
    return full_data.decode()


# The file which exist on the path will be sent
async def send_file(reader, writer, file_name):
    '''
        TODO: send file to Server
    '''    
    if os.path.exists(file_name):
        # If there is a file on the path
        await send_message(writer, "create\n")
        length = 0
        with open(file_name, 'r') as f:
            # Open A file and Get the file length
            length = len(f.readlines())
            await send_message(writer, str(length) + '\n')
        with open(file_name, 'r') as f:
            await send_message(writer, f.read())
    else:
        await send_message(writer, "NAK: File Doesn't Exist in Server\n")

# The file will be created that sent by client
async def create_file(reader, length, file_name):
    with open(file_name, 'w') as f:
            file_content = await receive_long_message(reader)
            f.write(file_content)
    return

async def remove_file(writer, file_name):
    if os.path.exists(file_name):
        # There is no any file to be removed 
        await send_message(writer, "remove\n")
        os.remove(file_name)
    else:
        await send_message(writer, "NAK: File To Remove Doesn't Exist\n")
    return

async def handle_client(reader, writer):

    # password can not be used
    """
    pw = "1234"
    count = 0
    user_pw = str()
    while(count < 3):
        user_pw = await receive_long_message(reader)
        print(user_pw)
        if user_pw == pw:
            await send_message(writer, "Success\n")
            break
        await send_message(writer, "Failed\n")
        count += 1
        if count == 3:
            writer.close()
            await writer.wait_closed()
        continue
    """

    # message print out
    await send_intro_message(writer)
    await send_bash_intro(writer)

    # TODO: Client Access 
    
    while(1):
        user_input = await receive_long_message(reader)
        print("User Input: " + user_input)
        user_input = user_input.split(' ')
        # list
        if user_input[0] == "list":
            await send_message(writer, "ACK\n")
            li = os.listdir("./")
            await send_message(writer, li)
            continue
        # Client Send File to Client
        elif user_input[0] == "put":
            await send_message(writer, "upload\n")
            length = await receive_long_message(reader)
            length = int(length)
            await create_file(reader, length, user_input[1])
            continue
        # Server Send file to Server
        elif user_input[0] == "get":
            await send_file(reader, writer, user_input[1])
            continue
        elif user_input[0] == "remove":
            await remove_file(writer, user_input[1])
            continue
        elif user_input[0] == "close":
            await send_message(writer, "Close Connection\n")
            writer.close()
            await writer.wait_closed()
            break
        else:
            await send_file(reader, writer, "NAK: Wrong Command\n")
            continue

async def main():
    server = await asyncio.start_server(
            handle_client,
            INTERFACE, SPORT
    )
    async with server:
        await server.serve_forever()

# Run the `main()` function
if __name__ == "__main__":
    asyncio.run(main())
