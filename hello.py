#!/usr/bin/python

import cgi
import cgitb
import socket
import backend

cgitb.enable()

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from maq1 fields
if form.getvalue('maq1_ps'):
        maq1_ps_flag = "ON"
        maq1_ps_text = form.getvalue('maq1-ps')
else:
        maq1_ps_flag = "OFF"

if form.getvalue('maq1_df'):
        maq1_df_flag = "ON"
        maq1_df_text = form.getvalue('maq1-df')
else:
        maq1_df_flag = "OFF"

if form.getvalue('maq1_finger'):
        maq1_finger_flag = "ON"
        maq1_finger_text = form.getvalue('maq1-finger')
else:
        maq1_finger_flag = "OFF"

if form.getvalue('maq1_uptime'):
        maq1_uptime_flag = "ON"
        maq1_uptime_text = form.getvalue('maq1-uptime')
else:
        maq1_uptime_flag = "OFF"

# Get data from maq2 fields
if form.getvalue('maq2_ps'):
        maq2_ps_flag = "ON"
        maq2_ps_text = form.getvalue('maq2-ps')
else:
        maq2_ps_flag = "OFF"

if form.getvalue('maq2_df'):
        maq2_df_flag = "ON"
        maq2_df_text = form.getvalue('maq2-df')
else:
        maq2_df_flag = "OFF"

if form.getvalue('maq2_finger'):
        maq2_finger_flag = "ON"
        maq2_finger_text = form.getvalue('maq2-finger')
else:
        maq2_finger_flag = "OFF"

if form.getvalue('maq2_uptime'):
        maq2_uptime_flag = "ON"
        maq2_uptime_text = form.getvalue('maq2-uptime')
else:
        maq2_uptime_flag = "OFF"

# Get data from maq3 fields
if form.getvalue('maq3_ps'):
        maq3_ps_flag = "ON"
        maq3_ps_text = form.getvalue('maq3-ps')
else:
        maq3_ps_flag = "OFF"

if form.getvalue('maq3_df'):
        maq3_df_flag = "ON"
        maq3_df_text = form.getvalue('maq3-df')
else:
        maq3_df_flag = "OFF"

if form.getvalue('maq3_finger'):
        maq3_finger_flag = "ON"
        maq3_finger_text = form.getvalue('maq3-finger')
else:
        maq3_finger_flag = "OFF"

if form.getvalue('maq3_uptime'):
        maq3_uptime_flag = "ON"
        maq3_uptime_text = form.getvalue('maq3-uptime')
else:
        maq3_uptime_flag = "OFF"

# Create a data list for each machine
data1 = [] # Data list for maq1
data2 = [] # Data list for maq2
data3 = [] # Data list for maq3

# Create socket for maq1
# Initialize packet sequence number
SEQ_NUMBER = 0
# Create socket
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect(('localhost', 8888))
# Initialize text variable for use in case the corresponding box wasn't checked
text = ''

# Iterate over list of commands to determine which ones have their boxes checked
# In case any of them does, get its text and create and send a packet with the command 
for index, command_type in enumerate(['ps', 'df', 'finger', 'uptime']):
        if command_type == 'ps':
                flag = maq1_ps_flag
                if flag == "ON":
                        text = maq1_ps_text
        elif command_type == 'df':
                flag = maq1_df_flag
                if flag == "ON":
                        text = maq1_df_text
        elif command_type == 'finger':
                flag = maq1_finger_flag
                if flag == "ON":
                        text = maq1_finger_text
        elif command_type == 'uptime':
                flag = maq1_uptime_flag
                if flag == "ON":
                        text = maq1_uptime_text
        # If the corresponding box was selected
        if flag == "ON":
                # Create packet
                Packet = backend.CreatePacket(text, SEQ_NUMBER, command_type)
                # Update sequence number
                SEQ_NUMBER += 1
                # Send packet
                s1.send(Packet)

                # Receive data to publish on webpage
                data1.append(s1.recv(1024))
        else:
                data1.append('')
# Close socket
s1.close()

# Create socket for maq2
# Reinitialize packet sequence number
SEQ_NUMBER = 0
# Create socket
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(('localhost', 8887))

# Initialize text variable for use in case the corresponding box isn't checked
text = ''

# Iterate over list of commands to determine which ones have their boxes checked
# If any of them does, get its text and create and send a packet with the command
for index, command_type in enumerate(['ps', 'df', 'finger', 'uptime']):
        if command_type == 'ps':
                flag = maq2_ps_flag
                if flag == "ON":
                        text = maq2_ps_text
        elif command_type == 'df':
                flag = maq2_df_flag
                if flag == "ON":
                        text = maq2_df_text
        elif command_type == 'finger':
                flag = maq2_finger_flag
                if flag == "ON":
                        text = maq2_finger_text
        elif command_type == 'uptime':
                flag = maq2_uptime_flag
                if flag == "ON":
                        text = maq2_uptime_text
        # If the corresponding box was selected
        if flag == "ON":
                # Create packet
                Packet = backend.CreatePacket(text, SEQ_NUMBER, command_type)
                # Update sequence number
                SEQ_NUMBER += 1
                # Send packet
                s2.send(Packet)

                # Receive data to publish on webpage
                data2.append(s2.recv(1024))
        else:
                data2.append('')
# Close socket
s2.close()

# Create socket for maq3
# Reinitialize packet sequence number
SEQ_NUMBER = 0
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3.connect(('localhost', 8886))

# Initialize text variable for use in case the corresponding box wasn't checked
text = ''

# Iterate over list of commands to determine which ones have their boxes checked
# If any of them does, get its text and create and send a packet with the command
for index, command_type in enumerate(['ps', 'df', 'finger', 'uptime']):
        if command_type == 'ps':
                flag = maq3_ps_flag
                if flag == "ON":
                        text = maq3_ps_text
        elif command_type == 'df':
                flag = maq3_df_flag
                if flag == "ON":
                        text = maq3_df_text
        elif command_type == 'finger':
                flag = maq3_finger_flag
                if flag == "ON":
                        text = maq3_finger_text
        elif command_type == 'uptime':
                flag = maq3_uptime_flag
                if flag == "ON":
                        text = maq3_uptime_text
        # If the corresponding box was selected
        if flag == "ON":
                # Create packet
                Packet = backend.CreatePacket(text, SEQ_NUMBER, command_type)
                # Update sequence number
                SEQ_NUMBER += 1
                # Send packet
                s3.send(Packet)

                # Receive data to publish on webpage
                data3.append(s3.recv(1024))
        else:
                data3.append('')
# Close socket
s3.close()

print("Content-Type: text/html;charset=utf-8\r\n\r\n")

# Print maq1 data

print("<b>MAQ 1</b><br />")

# If the corresponding box is checked, print ps data
if maq1_ps_flag == "ON":
        print("<p><b>ps</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data1[0])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print df data
if maq1_df_flag == "ON":
        print("<p><b>df</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data1[1])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print finger data
if maq1_finger_flag == "ON":
        print("<p><b>finger</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data1[2])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print uptime data
if maq1_uptime_flag == "ON":
        print("<p><b>uptime</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data1[3])
        print("</pre>")
        print("<br /> </p>")

# Print maq2 data

print("<b>MAQ 2</b><br />")

# If the corresponding box is checked, print ps data
if maq2_ps_flag == "ON":
        print("<p><b>ps</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data2[0])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print df data
if maq2_df_flag == "ON":
        print("<p><b>df</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data2[1])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print finger data
if maq2_finger_flag == "ON":
        print("<p><b>finger</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data2[2])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print uptime data
if maq2_uptime_flag == "ON":
        print("<p><b>uptime</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data2[3])
        print("</pre>")
        print("<br /> </p>")

# Print maq3 data

print("<b>MAQ 3</b><br />")

# If the corresponding box is checked, print ps data
if maq3_ps_flag == "ON":
        print("<p><b>ps</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data3[0])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print df data
if maq3_df_flag == "ON":
        print("<p><b>df</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data3[1])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print finger data
if maq3_finger_flag == "ON":
        print("<p><b>finger</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data3[2])
        print("</pre>")
        print("<br /> </p>")

# If the corresponding box is checked, print uptime data
if maq3_uptime_flag == "ON":
        print("<p><b>uptime</b><br />")
        print("Output:<br />")
        print("<pre>")
        print(data3[3])
        print("</pre>")
        print("<br /> </p>")usr/bin/env python
