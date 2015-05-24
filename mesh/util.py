import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('gmail.com', 80))
    ip = s.getsockname()[0]
    s.close()

    return ip

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
