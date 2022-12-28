from unittest import TestCase

from encode_decode_executor import EncodeDecodeExecutor
from protobuf_encode_decoder import ProtobufEncoderDecoder
import pytest


class ProtoBufEncodeDecodeTestCase(TestCase):
    def setUp(self) -> None:
        self.protocol_buffer_enc_dec = ProtobufEncoderDecoder()

    def test_encode_hello_message(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {
            "type": "status",
            "msg": "send me count please",
            "client_host": "0.0.0.0",
            "identifier": 1234,
            "client_port": 4000,
        }
        encoded_binary = encoder_decoder.encode_hello(msg_dict)
        assert encoded_binary == b'\n\x06status\x12\x14send me count please\x1a\x070.0.0.0 \xa0\x1f(\xd2\t'

    def test_encode_decode_hello_message(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {
            "type": "status",
            "msg": "send me count please",
            "client_host": "0.0.0.0",
            "identifier": 1234,
            "client_port": 4000,
        }
        encoded_binary = encoder_decoder.encode_hello(msg_dict)
        decoded_message = encoder_decoder.decode_hello(encoded_binary)

        assert decoded_message == msg_dict

    def test_encode_status_message(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {"type": "status",
                    "message_count": 100,
                    "identifier": 1234
                    }
        encoded_binary = encoder_decoder.encode_status(msg_dict)
        assert encoded_binary == b'\n\x06status\x10d\x18\xd2\t'

    def test_encode_decode_status_message(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {"type": "status",
                    "message_count": 100,
                    "identifier": 1234
                    }
        encoded_binary = encoder_decoder.encode_status(msg_dict)
        decoded_message = encoder_decoder.decode_status(encoded_binary)
        assert decoded_message == msg_dict

    def test_encode_hello_with_wrong_message(self):

        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {"type": "status",
                    "message_count": 100,
                    "identifier": 1234
                    }
        # incorrect message for encode_hello() and expect exception raise
        with pytest.raises(TypeError):
            encoder_decoder.encode_hello(msg_dict)

