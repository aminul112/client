import asyncio
from unittest import TestCase

from client import Client
from encode_decode_executor import EncodeDecodeExecutor
from protobuf_encode_decoder import ProtobufEncoderDecoder


class TestClientIntegration(TestCase):
    def test_send_a_message_to_server(self):
        encoder_decoder = EncodeDecodeExecutor(ProtobufEncoderDecoder())
        client_identifier = 7777
        client_port = 2222
        client_ip = "0.0.0.0"
        server_ip = "0.0.0.0"
        server_port = 4000
        client = Client(
            encoder_decoder=encoder_decoder,
            client_identifier=client_identifier,
            client_port=client_port,
            client_ip=client_ip,
            server_ip=server_ip,
            server_port=server_port,
        )
        msg = {
            "type": "heartbeat",
            "msg": "I’m here!",
            "identifier": client_identifier,
            "client_host": server_ip,
            "client_port": client_port,
        }
        loop = asyncio.get_event_loop()

        result = loop.run_until_complete(
            client.send_a_message_to_server(
                server_ip=server_ip, server_port=server_port, msg=msg
            )
        )
        loop.close()
        self.assertEqual(
            result,
            {
                "client_host": "0.0.0.0",
                "client_port": 2222,
                "identifier": 7777,
                "msg": "ack",
                "type": "heartbeat",
            },
        )
