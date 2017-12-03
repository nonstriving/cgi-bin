import socket
import sys
from thread import *
import struct
import os 
from backend import crc16
import time
         
HOST = ''
PORT = int(sys.argv[1])
             
if (PORT != 8888) and (PORT != 8887) and (PORT != 8886):
        print 'Trying to use invalid port'
        sys.exit()
    
# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created on port ' + str(PORT)
    
# Bind socket
try:
        s.bind((HOST, PORT))
except socket.error as msg:
        print 'Bind failed with error code: ' + str(msg[0]) + ' Message: ' + msg[1]
        sys.exit()
print 'Bind successful'

s.listen(10)

# Create a thread
def CreateThread(connection):
        while True:
                packet = connection.recv(1024)
                if not packet:
                        break

                # Parsing of packet
                # Index of first byte in the options field
                options_index = struct.calcsize('!BBBHHBHBB16s16s16s')
                # Data (options field)
                options = packet[options_index:]
                # Header
                header = packet[:options_index]
                # Unpack header data to obtain the header fields
                Version, IHL, Type_of_service, Total_length, Identification, Flags, Fragment_offset, Time_to_live, Protocol, Header_checksum, Source_address, Destination_address = struct.unpack('!BBBHHBHBB16s16s16s', header)
                print Version
                print IHL
                print Type_of_service
                print Total_length
                print Identification
                print Fragment_offset
                print Time_to_live
                print Protocol
                print Source_address
                print Destination_address
                # Pack checksum data (header minus checksum field) to provide as argument for crc16()
                local_checksum_data = struct.pack('!BBBHHBHBB16s16s', Version, IHL, Type_of_service, Total_length, Identification, Flags, Fragment_offset, Time_to_live, Protocol, Source_address, Destination_address)
                # Calculate checksum
                local_checksum = crc16(local_checksum_data)
                print 'Calculated checksum value: ' + local_checksum
                # Received checksum value
                remote_checksum = Header_checksum
                print 'Received checksum value: ' + remote_checksum

                # Get command code from the appropriate header field
                code = Protocol

                if code == 1:
                        command_type = 'ps'
                elif code == 2:
                        command_type = 'df'
                elif code == 3:
                        command_type = 'finger'
                elif code == 4:
                        command_type = 'uptime'

                # Check for malicious characters in the command
                if '|' in options or ';' in options or '>' in options:
                        output = 'Error: trying to execute malicious command'
                else:
                        # Execute command on daemon process
                        f = os.popen(command_type + ' ' + options)
                        output = f.read()
                print output

                # Execute command on daemon process
                f = os.popen(command_type + ' ' + options)
                output = f.read()
                print output

                # Send output of command through the connection
                connection.sendall(output)

        connection.close()

while True:
        # Accept connection
        connection, address = s.accept()
        print 'Connected to ' + address[0] + ':' + str(address[1])
        # Start a thread
        start_new_thread(CreateThread, (connection,))

# Close socket
s.close()
