import socket
import struct
import sys

message = 'very important data'
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)

#The socket also needs to be configured with a time-to-live value (TTL) for the messages. The TTL controls how many networks will receive the packet. Set the TTL with the IP_MULTICAST_TTL option and setsockopt(). The default, 1, means that the packets are not forwarded by the router beyond the current network segment. The value can range up to 255, and should be packed into a single byte.

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

#The rest of the sender looks like the UDP echo client, except that it expects multiple responses so uses a loop to call 
# recvfrom() until it times out.

try:

    # Send data to the multicast group
    #print >>sys.stderr, 'sending "%s"' % message
    print('sending "%s"' % message, file=sys.stderr)
    sent = sock.sendto(bytes(message,'ascii'), multicast_group)

    # Look for responses from all recipients
    while True:
        print ('waiting to receive', file=sys.stderr)
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print ('timed out, no more responses', file=sys.stderr)
            break
        else:
            print ('received "%s" from %s' % (data, server),file=sys.stderr)

finally:
    print ('closing socket', file=sys.stderr)
    sock.close()

 