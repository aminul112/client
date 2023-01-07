import asyncio
import logging

from encode_decode_executor import EncodeDecodeExecutor

log = logging.getLogger("client_log")
heartbeat_count = 0


class Client:
    def __init__(
        self,
        encoder_decoder: EncodeDecodeExecutor,
        client_identifier: int,
        client_port: int,
    ):
        self.encoder_decoder = encoder_decoder
        self.client_identifier = client_identifier
        self.client_port = client_port

    async def accept_client(self, client_port: int):
        log.info(f"accept_client: serving as client {client_port}")
        await asyncio.start_server(
            self.handle_server_request,
            "0.0.0.0",
            client_port,
        )

    async def handle_server_request(
        self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter
    ):
        log.info("handle_server_request: serving as a SERVER:")

        data = await client_reader.read(1024)
        if not data:
            log.error("socket closed: could not read server request")
            raise Exception("socket closed: could not read server request")

        deserialized_dict = self.encoder_decoder.decode_status(binary_data=data)
        log.info(f"received a request from server: {deserialized_dict}")

        status_msg = {
            "type": "status",
            "message_count": heartbeat_count,
            "identifier": self.client_identifier,
        }

        serialized_status = self.encoder_decoder.encode_status(msg_dict=status_msg)
        log.info("Serialized Status message count sending to Server ")
        client_writer.write(serialized_status)
        await client_writer.drain()

        # wait for ACK message
        data = await client_reader.read(1024)

        if data is None:
            log.error("socket closed: could not read ACK from server")
            raise Exception("socket closed: could not read ACK from server")

        deserialized_dict = self.encoder_decoder.decode_heartbeat(binary_data=data)
        log.info(f"received ACK message is {deserialized_dict}")

        await client_writer.drain()

    async def handle_client(self, server_ip: str, server_port: int, msg: dict):
        await self.send_a_message_to_server(
            server_ip=server_ip, server_port=server_port, msg=msg
        )

    async def send_heartbeat_message(self, interval: int, func, *args, **kwargs):
        """Run func every interval seconds."""
        while True:
            await asyncio.gather(
                func(*args, **kwargs),
                asyncio.sleep(interval),
            )

    async def send_a_message_to_server(
        self, server_ip: str, server_port: int, msg: dict
    ):
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

    async def heartbeat(self, server_ip: str, server_port: int, client_identifier: int):
        log.info(f"sending heartbeat to: {server_ip}:{server_port}")
        msg = {
            "type": "heartbeat",
            "msg": "I’m here!",
            "identifier": client_identifier,
            "client_host": server_ip,
            "client_port": self.client_port,
        }
        global heartbeat_count
        heartbeat_count = heartbeat_count + 1
        await self.send_a_message_to_server(
            server_ip=server_ip, server_port=server_port, msg=msg
        )
