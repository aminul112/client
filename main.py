import asyncio
import logging

from client import Client
from encode_decode_executor import EncodeDecodeExecutor
from protobuf_encode_decoder import ProtobufEncoderDecoder
from dotenv import load_dotenv
import os

load_dotenv()

log = logging.getLogger("client_log")


async def main():
    server_ip = os.getenv("SERVER_IP")
    server_port = int(os.getenv("SERVER_PORT"))
    client_ip = os.getenv("CLIENT_IP")
    client_port = int(os.getenv("CLIENT_PORT"))
    client_identifier = int(os.getenv("CLIENT_IDENTIFIER"))
    heartbeat_interval = int(os.getenv("HEARTBEAT_INTERVAL_SECONDS", 60))

    if not (server_ip and server_port and client_ip and client_port and client_identifier):
        log.error(".env file must have valid SERVER_IP, SERVER_PORT, CLIENT_IP, CLIENT_PORT and CLIENT_IDENTIFIER  "
                  "defined")
        return

    log.info(f"server ip is {server_ip} server port is {server_port}")
    log.info(f"client ip is {client_ip} client port is {client_port}")
    log.info(f"client_identifier  is {client_identifier}")
    log.info(f"heartbeat_interval  is {heartbeat_interval}")

    encoder_decoder = EncodeDecodeExecutor(ProtobufEncoderDecoder())
    client = Client(encoder_decoder=encoder_decoder, client_identifier=client_identifier, client_port=client_port)

    log.info(f"MAIN begin: {server_ip} {server_port} {client_port} {client_identifier}")
    loop = asyncio.get_event_loop()
    try:
        msg = {"type": "heartbeat",
               "msg": "First Message",
               "client_host": client_ip,
               "client_port": client_port,
               "identifier": client_identifier}

        await client.handle_client(server_ip, server_port, msg)
    except Exception as ex:
        log.error(f"Main function exception happened {ex}")

    f2 = asyncio.ensure_future(client.accept_client(client_port=client_port))
    await f2
    t2 = asyncio.ensure_future(
        client.send_heartbeat_message(heartbeat_interval, client.heartbeat, server_ip, server_port, client_identifier))
    await t2
    loop.run_forever()

    log.info("MAIN end")


if __name__ == '__main__':
    logging.basicConfig(filename='log/client.log', encoding='utf-8', level=logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(levelname)s " +
                                  "[%(module)s:%(lineno)d] %(message)s")

    # setup console logging
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    log.addHandler(ch)
    asyncio.run(main())
