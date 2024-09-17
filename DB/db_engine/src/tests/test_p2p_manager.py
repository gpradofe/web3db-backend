import unittest
import asyncio
from src.p2p_manager import P2PManager

class TestP2PManager(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.p2p_manager = P2PManager()

    def test_start(self):
        self.loop.run_until_complete(self.p2p_manager.start())
        self.assertIsNotNone(self.p2p_manager.host)
        self.assertIsNotNone(self.p2p_manager.pubsub)

    def test_connect_to_peer(self):
        self.loop.run_until_complete(self.p2p_manager.start())
        peer_addr = "/ip4/127.0.0.1/tcp/8000/p2p/QmYyQSo1c1Ym7orWxLYvCrM2EmxFTANf8wXmmE7DWjhx5N"
        result = self.loop.run_until_complete(self.p2p_manager.connect_to_peer(peer_addr))
        self.assertTrue(result)

    def test_broadcast_presence(self):
        self.loop.run_until_complete(self.p2p_manager.start())
        self.loop.run_until_complete(self.p2p_manager.broadcast_presence())
        # This test just ensures that the broadcast doesn't raise an exception

    def test_get_connected_peers(self):
        self.loop.run_until_complete(self.p2p_manager.start())
        peers = self.p2p_manager.get_connected_peers()
        self.assertIsInstance(peers, list)

if __name__ == '__main__':
    unittest.main()