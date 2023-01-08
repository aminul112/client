import asyncio
import logging

from encode_decode_executor import EncodeDecodeExecutor

log = logging.getLogger("__main__." + __name__)


class Client:
    def __init__(
        self,
        encoder_decoder: EncodeDecodeExecutor,
        client_identifier: int,
        client_port: int,
        client_ip: str,
        server_ip: str,
        server_port: int,
    ):
        self.encoder_decoder = encoder_decoder
        self.client_identifier = client_identifier
        self.client_port = client_port
        self.client_ip = client_ip
        self.server_ip = server_ip
        self.server_port = server_port
        self.heartbeat_count = 0

    async def start_server(self) -> None:
        """
        This method starts a server to handle status message request from the server.
        """
        log.info(f"start_server: starting a server with port {self.client_port}")
        await asyncio.start_server(
            self.handle_server_request,
            self.client_ip,
            self.client_port,
        )

    async def handle_server_request(
        self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter
    ) -> None:
        """
        This is callback function for start_server() function of asyncio.
        :param client_reader: StreamReader object to read data from client.
        :param client_writer: StreamWriter object to write data to client.
        """
        log.info("handle_server_request: serving as a SERVER:")

        data = await client_reader.read(1024)
        if not data:
            log.error("socket closed: could not read server request")
            raise Exception("socket closed: could not read server request")

        deserialized_dict = self.encoder_decoder.decode_status(binary_data=data)
        log.info(f"received a request from server: {deserialized_dict}")

        status_msg = {
            "type": "status",
            "message_count": self.heartbeat_count,
            "identifier": self.client_identifier,
        }

        serialized_status = self.encoder_decoder.encode_status(msg_dict=status_msg)
        log.info("Serialized Status message count sending to Server ")
        client_writer.write(serialized_status)
        await client_writer.drain()

        # wait for ack message
        data = await client_reader.read(1024)

        if data is None:
            log.error("socket closed: could not read ack from server")
            raise Exception("socket closed: could not read ack from server")

        deserialized_dict = self.encoder_decoder.decode_heartbeat(binary_data=data)
        log.info(f"received ack message is {deserialized_dict}")

        await client_writer.drain()

    async def send_to_server(self, server_ip: str, server_port: int, msg: dict) -> None:
        """
        A wrapper function to send first message to server.
        :param server_ip: server ip address
        :param server_port: server port number
        :param msg: the message to send
        """

        await self.send_a_message_to_server(
            server_ip=server_ip, server_port=server_port, msg=msg
        )

    async def send_heartbeat_message(self, interval: int, func, *args, **kwargs):
        """
        Run func every interval seconds. Runs forever.

        :param interval: interval in seconds.
        :param func: function to use.
        """
        while True:
            await asyncio.gather(
                func(*args, **kwargs),
                asyncio.sleep(interval),
            )

    async def send_a_message_to_server(
        self, server_ip: str, server_port: int, msg: dict
    ):
        """
        Serves message sending to the server.
        :param server_ip: server ip address
        :param server_port: server port number
        :param msg: the message to send
        """

        try:

            client_reader, client_writer = await asyncio.open_connection(
                server_ip, server_port
            )

            serialized_bnr = self.encoder_decoder.encode_heartbeat(msg_dict=msg)

            log.info(f"Client connected sending data {msg}")

            client_writer.write(serialized_bnr)
            await client_writer.drain()

            data = await client_reader.read(1024)
            if not data:
                log.error("socket closed: server did not reply")
                raise Exception("socket closed: server did not reply")

            deserialized_obj = self.encoder_decoder.decode_heartbeat(binary_data=data)
            log.info(
                f"deserialized heartbeat reply data from server is {deserialized_obj}"
            )

            client_writer.close()
        except (ConnectionError, OSError) as e:
            log.error(f"Connection error while sending heartbeat{e}")

    async def send_heartbeat(self) -> None:
        """
        This function is called by send_heartbeat_message(), see main.py with an interval.
        This function send message to server. Keeps heartbeat message count.
        """
        log.info(f"sending heartbeat to: {self.server_ip}:{self.server_port}")
        msg = {
            "type": "heartbeat",
            "msg": "I’m here!",
            "identifier": self.client_identifier,
            "client_host": self.server_ip,
            "client_port": self.client_port,
        }

        self.heartbeat_count = self.heartbeat_count + 1
        await self.send_a_message_to_server(
            server_ip=self.server_ip, server_port=self.server_port, msg=msg
        )
