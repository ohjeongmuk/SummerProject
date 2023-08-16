## Instruction
The files are broadly divided into server file zip and client file zip. Please note that the user manual differs depending on the type of zip file opened.


## How to Use
This file is a client file. The server file will be opened on the school flip1 server. This file will be executed in your local environment. So please compile this file in your working environment.

### install and run

1. Python version check
    There are no lines of code related to MongoDB in the client file, but it is important to have the same python version as the server side.

    `python3 --version`

2. Two bashshells
    One bash shell will run ftp_client.py. And we need one more bash shell to forward to the flip server 8085 port.

3. Code Execution
    First, enter the following code to forward to the flip server 8085 port.

    `ssh -NL 8085:localhost:8080 ONID@flip1.engr.oregonstate.edu`

    (ex: `ssh -NL 8085:localhost:8080 ohjeo@flip1.engr.oregonstate.edu`)

    Second, run ftp_client.
    `python3 ftp_client.py`

4. Example client code

To server: `list`
>> serverfile.txt

To server: `get serverfile.txt`
>> File Downloading...
(Check myfiles folder)

To server: `put clientfile.txt`
>> uploading..
>> Title: `Harry Porter`
>> Author: `JK Rowling`

To server: `close`
>> done