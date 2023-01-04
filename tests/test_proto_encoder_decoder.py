from unittest import TestCase

from encode_decode_executor import EncodeDecodeExecutor
from protobuf_encode_decoder import ProtobufEncoderDecoder


class ProtoBufEncodeDecodeTestCase(TestCase):
    def setUp(self) -> None:
        self.protocol_buffer_enc_dec = ProtobufEncoderDecoder()

    def test_encode_hello_message(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {
            "type": "heartbeat",
            "msg": "send me count please",
            "client_host": "0.0.0.0",
            "identifier": 1234,
            "client_port": 4000,
        }
        encoded_binary = encoder_decoder.encode_heartbeat(msg_dict)
        assert encoded_binary == b'\n\theartbeat\x12\x14send me count please\x1a\x070.0.0.0 \xa0\x1f(\xd2\t'

    def test_encode_decode_hello_message(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {
            "type": "heartbeat",
            "msg": "send me count please",
            "client_host": "0.0.0.0",
            "identifier": 1234,
            "client_port": 4000,
        }
        encoded_binary = encoder_decoder.encode_heartbeat(msg_dict)
        decoded_message = encoder_decoder.decode_heartbeat(encoded_binary)

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
        # incorrect message for encode_heartbeat() and expect error
        encoded_binary = encoder_decoder.encode_heartbeat(msg_dict)
        assert encoded_binary == (b'\n\x05error\x12\x80\x01Cannot set HeartBeatMessage.msg to None: None has '
 b"type <class 'NoneType'>, but expected one of: (<class 'bytes'>, <class 'str'"
 b'>)')

    def test_encode_correctly_but_decode_with_incorrect_message(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {"type": "status",
                    "message_count": 100,
                    "identifier": 1234
                    }
        encoded_binary = encoder_decoder.encode_status(msg_dict)

        # decode with a wrong decoder
        decoded_message = encoder_decoder.decode_heartbeat(encoded_binary)
        assert decoded_message == {
            "type": "error",
            "msg": "incorrect decoder"
        }

    def test_encode_hello_message_but_decode_status(self):
        encoder_decoder = EncodeDecodeExecutor(self.protocol_buffer_enc_dec)
        msg_dict = {
            "type": "hello",
            "msg": "send me count please",
            "client_host": "0.0.0.0",
            "identifier": 1234,
            "client_port": 4000,
        }
        encoded_binary = encoder_decoder.encode_heartbeat(msg_dict)
        # decode with a wrong decoder
        decoded_message = encoder_decoder.decode_status(encoded_binary)
        assert decoded_message == {
            "type": "error",
            "msg": "incorrect decoder"
        }
