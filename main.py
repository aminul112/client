import asyncio
import logging

from client import Client
from encode_decode_executor import EncodeDecodeExecutor
from protobuf_encode_decoder import ProtobufEncoderDecoder
from dotenv import load_dotenv
import os

load_dotenv()

log = logging.getLogger()


async def main():
    server_ip = os.getenv("SERVER_IP", "0.0.0.0")
    server_port = int(os.getenv("SERVER_PORT", 4000))
    client_ip = os.getenv("CLIENT_IP", "0.0.0.0")
    client_port = int(os.getenv("CLIENT_PORT", 3000))
    client_identifier = int(os.getenv("CLIENT_IDENTIFIER", 1234))
    heartbeat_interval = int(os.getenv("HEARTBEAT_INTERVAL_SECONDS", 60))

    log.info(f"server ip is {server_ip} server port is {server_port}")
    log.info(f"client ip is {client_ip} client port is {client_port}")
    log.info(f"client_identifier  is {client_identifier}")
    log.info(f"heartbeat_interval  is {heartbeat_interval}")

    encoder_decoder = EncodeDecodeExecutor(ProtobufEncoderDecoder())
    client = Client(
        encoder_decoder=encoder_decoder,
        client_identifier=client_identifier,
        client_port=client_port,
        client_ip=client_ip,
        server_ip=server_ip,
        server_port=server_port,
    )

    log.info(f"MAIN begin: {server_ip} {server_port} {client_port} {client_identifier}")
    loop = asyncio.get_event_loop()
    try:
        msg = {
            "type": "heartbeat",
            "msg": "First Message",
            "client_host": client_ip,
            "client_port": client_port,
            "identifier": client_identifier,
        }

        await client.send_to_server(server_ip, server_port, msg)
    except Exception as ex:
        log.error(f"Main function exception happened {ex}")

    f2 = asyncio.ensure_future(client.accept_client())
    await f2
    t2 = asyncio.ensure_future(
        client.send_heartbeat_message(
            heartbeat_interval,
            client.send_heartbeat,
        )
    )
    await t2
    loop.run_forever()

    log.info("MAIN end")


if __name__ == "__main__":
    logging.basicConfig(
        filename="log/client.log", encoding="utf-8", level=logging.DEBUG
    )

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s " + "[%(module)s:%(lineno)d] %(message)s"
    )

    # setup console logging
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    log.addHandler(ch)
    asyncio.run(main())
