#!/usr/bin/env python

import cgi
import cgitb
import socket
import struct

# Return size of string in bytes
def SizeInBytes(string):
        if string == None:
                size = 0
        else:
                size = len(string.encode('utf-8'))
        return size

# crc16 function
def crc16(header):
        # 16 bits long
        crc = 0xFFFF
        # generator value
        divisor = 0x1021
        for v1, v2 in zip(header[0::2], header[1::2]):
                crc = crc ^ struct.unpack("!H", v1 + v2)[0]

        for i in range(0, 8):
                if(crc & 0x8000) != 0:
                        crc = ((crc << 1) ^ divisor)
                else:
                        crc = crc << 1
        return str(crc)

def CreatePacket(text, seq_number, command_type):
        # Options field
        Data = text

        # Header
        Version = 2
        IHL = 20
        Type_of_service = 0
        Total_length = IHL + SizeInBytes(text)
        Identification = seq_number # sequence number
        Flags = 0 # 000 if request, 111 if reply
        Fragment_offset = 0
        Time_to_live = 255
        if command_type == 'ps':
                Protocol = 1
        elif command_type == 'df':
                Protocol = 2
        elif command_type == 'finger':
                Protocol = 3
        elif command_type == 'uptime':
                Protocol = 4
        # Protocol is: 1 for ps, 2 for df, 3 for finger, 4 for uptime
        Source_address = '192.168.56.101'
        Destination_address = '192.168.56.101'
        # Header data used to calculate checksum
        Checksum_data = struct.pack('!BBBHHBHBB16s16s', Version, IHL, Type_of_service, Total_length, Identification, Flags, Fragment_offset, Time_to_live, Protocol, Source_address, Destination_address)
        # Calculate checksum value
        Header_checksum = crc16(Checksum_data)

        if Data == None:
                Data = ''

        # Header including checksum value
        Header = struct.pack('!BBBHHBHBB16s16s16s', Version, IHL, Type_of_service, Total_length, Identification, Flags, Fragment_offset, Time_to_live, Protocol, Header_checksum, Source_address, Destination_address)

        # Concatenate header and data (options field)
        Packet = Header + Data

        return Packet
