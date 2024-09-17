import asyncio
from libp2p import new_host
from libp2p.peer.peerinfo import info_from_p2p_addr
from libp2p.pubsub.pubsub import Pubsub
from libp2p.pubsub.gossipsub import GossipSub
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

class P2PManager:
    def __init__(self):
        self.host = None
        self.pubsub = None
        self.peers = set()
        self.config = Config.get_config()

    async def start(self):
        try:
            self.host = await new_host(
                transport_opt=[f"/ip4/0.0.0.0/tcp/{self.config['P2P_PORT']}"],
                muxer_opt=["/mplex/6.7.0"],
                sec_opt=["/secio"],
                enable_pubsub=True,
            )
            logger.info(f"P2P host started with ID: {self.host.get_id()}")
            
            self.pubsub = GossipSub(self.host)
            await self.pubsub.subscribe("node_discovery")
            
            for peer in self.config['KNOWN_PEERS']:
                if peer:
                    await self.connect_to_peer(peer)
        except Exception as e:
            logger.error(f"Failed to start P2P host: {str(e)}")
            raise

    async def connect_to_peer(self, peer_addr):
        try:
            peer_info = info_from_p2p_addr(peer_addr)
            await self.host.connect(peer_info)
            self.peers.add(str(peer_info.peer_id))
            logger.info(f"Connected to peer: {peer_info.peer_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to peer {peer_addr}: {str(e)}")
            return False

    async def broadcast_presence(self):
        try:
            message = json.dumps({
                "type": "presence",
                "node_id": str(self.host.get_id()),
                "addresses": [str(addr) for addr in self.host.get_addrs()]
            })
            await self.pubsub.publish("node_discovery", message.encode())
        except Exception as e:
            logger.error(f"Failed to broadcast presence: {str(e)}")

    async def listen_for_peers(self):
        while True:
            try:
                message = await self.pubsub.next_message()
                if message:
                    data = json.loads(message.data.decode())
                    if data["type"] == "presence" and data["node_id"] != str(self.host.get_id()):
                        logger.info(f"Discovered new peer: {data['node_id']}")
                        for addr in data["addresses"]:
                            await self.connect_to_peer(addr)
            except Exception as e:
                logger.error(f"Error in listen_for_peers: {str(e)}")
            await asyncio.sleep(1)

    def get_connected_peers(self):
        return list(self.peers)

    async def run(self):
        await self.start()
        await self.broadcast_presence()
        asyncio.create_task(self.listen_for_peers())

        while True:
            await asyncio.sleep(60)
            await self.broadcast_presence()

async def create_p2p_manager():
    manager = P2PManager()
    await manager.run()
    return manager