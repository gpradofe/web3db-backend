# p2p_manager.py

import asyncio
import threading
import logging
import ssl
import os

logger = logging.getLogger(__name__)

class P2PManager:
    def __init__(self, port, known_peers, certfile, keyfile, cafile):
        self.port = port
        self.known_peers = known_peers  # list of peer addresses (host:port)
        self.connected_peers = {}  # mapping of peer_id to (reader, writer)

        self.certfile = certfile
        self.keyfile = keyfile
        self.cafile = cafile

        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._start_loop, daemon=True)
        self.server = None

        # SSL Context for secure connections
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=self.cafile)
        self.ssl_context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        self.ssl_context.verify_mode = ssl.CERT_REQUIRED

    def start(self):
        self.thread.start()
        asyncio.run_coroutine_threadsafe(self._start_server(), self.loop)
        logger.info(f"P2P server starting on port {self.port}")

        # Optionally connect to known peers
        for peer_addr in self.known_peers:
            if peer_addr:
                self.connect_to_peer(peer_addr)

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _start_server(self):
        self.server = await asyncio.start_server(
            self.handle_connection,
            '0.0.0.0',  # Bind to all interfaces
            self.port,
            ssl=self.ssl_context
        )
        logger.info(f"P2P server started on port {self.port}")
    async def handle_connection(self, reader, writer):
        peer_cert = writer.get_extra_info('peercert')
        if not peer_cert:
            logger.error("No certificate provided by peer")
            writer.close()
            await writer.wait_closed()
            return

        peer_addr = writer.get_extra_info('peername')
        logger.info(f"Accepted secure connection from {peer_addr}")

        peer_id = self._get_peer_id_from_cert(peer_cert)
        self.connected_peers[peer_id] = (reader, writer)

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                message = data.decode().strip()
                logger.info(f"Received from {peer_id}: {message}")
                # Process the message here
                response = self._process_message(message)
                writer.write((response + '\n').encode())
                await writer.drain()
        except Exception as e:
            logger.error(f"Error handling connection from {peer_id}: {str(e)}")
        finally:
            logger.info(f"Closing connection from {peer_id}")
            writer.close()
            await writer.wait_closed()
            del self.connected_peers[peer_id]

    def connect_to_peer(self, peer_addr):
        future = asyncio.run_coroutine_threadsafe(self._connect_to_peer(peer_addr), self.loop)
        try:
            return future.result()
        except Exception as e:
            logger.error(f"Error connecting to peer {peer_addr}: {str(e)}")
            return False

    async def _connect_to_peer(self, peer_addr):
        try:
            host, port = peer_addr.split(':')
            reader, writer = await asyncio.open_connection(
                host,
                int(port),
                ssl=self.ssl_context
            )

            peer_cert = writer.get_extra_info('peercert')
            if not peer_cert:
                logger.error("No certificate provided by peer")
                writer.close()
                await writer.wait_closed()
                return False

            peer_id = self._get_peer_id_from_cert(peer_cert)
            self.connected_peers[peer_id] = (reader, writer)
            logger.info(f"Securely connected to peer {peer_id}")

            # Start handling communication with this peer
            asyncio.create_task(self._handle_peer(reader, writer, peer_id))
            return True
        except Exception as e:
            logger.error(f"Failed to connect to peer {peer_addr}: {str(e)}")
            return False

    async def _handle_peer(self, reader, writer, peer_id):
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                message = data.decode().strip()
                logger.info(f"Received from {peer_id}: {message}")
                # Process the message here
                response = self._process_message(message)
                writer.write((response + '\n').encode())
                await writer.drain()
        except Exception as e:
            logger.error(f"Error handling peer {peer_id}: {str(e)}")
        finally:
            logger.info(f"Closing connection to {peer_id}")
            writer.close()
            await writer.wait_closed()
            del self.connected_peers[peer_id]

    def get_connected_peers(self):
        return list(self.connected_peers.keys())

    def send_message_to_peer(self, peer_id, message):
        if peer_id in self.connected_peers:
            reader, writer = self.connected_peers[peer_id]
            writer.write((message + '\n').encode())
            asyncio.run_coroutine_threadsafe(writer.drain(), self.loop)
            logger.info(f"Sent to {peer_id}: {message}")
            return True
        else:
            logger.error(f"Peer {peer_id} not connected")
            return False

    def _process_message(self, message):
        # Implement your message processing logic here
        # For example, parse JSON messages and handle different actions
        try:
            # Example: Echo the message back
            return f"Echo: {message}"
        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")
            return "Error processing message"

    def _get_peer_id_from_cert(self, peer_cert):
        # Extract peer ID from certificate
        subject = dict(x[0] for x in peer_cert['subject'])
        common_name = subject.get('commonName')
        return common_name or "Unknown"

def create_p2p_manager():
    from .config import Config

    # Paths to your SSL/TLS certificate files
    certfile = Config['CERTFILE']
    keyfile = Config['KEYFILE']
    cafile = Config['CAFILE']

    # Ensure the certificate files exist
    if not os.path.exists(certfile) or not os.path.exists(keyfile) or not os.path.exists(cafile):
        raise FileNotFoundError("Certificate files not found")

    p2p_manager = P2PManager(
        port=Config['P2P_PORT'],
        known_peers=Config['KNOWN_PEERS'],
        certfile=certfile,
        keyfile=keyfile,
        cafile=cafile
    )
    p2p_manager.start()
    return p2p_manager
