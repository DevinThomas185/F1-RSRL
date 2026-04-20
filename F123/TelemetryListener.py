from F123 import Packets
import socket
import json

UDP_MAX_PACKET_SIZE = 2048

class TelemetryListener:
    __slots__ = [
        "__socket",
        "__udp_ip",
        "__udp_port",
    ]

    def __init__(self, udp_ip: str, udp_port: int) -> None:
        self.__socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )
        self.__socket.bind((udp_ip, udp_port))
        self.__socket.settimeout(1.0)  # Set a timeout for the socket operations
        self.__udp_ip = udp_ip
        self.__udp_port = udp_port
        print(f"Listening on {udp_ip}:{udp_port}")

    def stop_listening(self) -> None:
        self.__socket.close()
        print(f"Stopped listening on {self.__udp_ip}:{self.__udp_port}")

    def get(self) -> json:
        try:
            packet = self.__socket.recv(UDP_MAX_PACKET_SIZE)
            header = Packets.PacketHeader.from_buffer_copy(packet)
            key = (header.packet_format, header.packet_version, header.packet_id)
            return Packets.HEADER_FIELD_TO_PACKET_TYPE[key].unpack(packet)
        except socket.timeout:
            return None  # Return None on timeout to check stop event
        except OSError:  # Handle the case where the socket is closed
            return None
