import unittest
import asyncio
from unittest.mock import patch, MagicMock
from src.p2p_manager import P2PManager, create_p2p_manager
import ssl

class TestP2PManager(unittest.IsolatedAsyncioTestCase):
    @patch('ssl.create_default_context')
    async def asyncSetUp(self, mock_create_context):
        mock_context = MagicMock()
        mock_create_context.return_value = mock_context
        self.p2p_manager = P2PManager(port=7175, known_peers=['peer1:7176', 'peer2:7177'], certfile='path/to/cert.pem', keyfile='path/to/key.pem', cafile='path/to/ca.pem')
        await self.p2p_manager.start()

    async def asyncTearDown(self):
        await self.p2p_manager.stop()

    async def test_start(self):
        self.assertIsNotNone(self.p2p_manager.server)
        self.assertIsNotNone(self.p2p_manager.ssl_context)

    @patch('asyncio.open_connection')
    async def test_connect_to_peer(self, mock_open_connection):
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        result = await self.p2p_manager._connect_to_peer('peer3:7178')
        self.assertTrue(result)
        self.assertIn('peer3:7178', self.p2p_manager.connected_peers)

    async def test_get_connected_peers(self):
        self.p2p_manager.connected_peers = {
            'peer1': (MagicMock(), MagicMock()),
            'peer2': (MagicMock(), MagicMock())
        }
        peers = self.p2p_manager.get_connected_peers()
        self.assertEqual(set(peers), {'peer1', 'peer2'})

    @patch.object(P2PManager, '_process_message')
    async def test_handle_connection(self, mock_process_message):
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.readline.side_effect = [b'Hello\n', b'']
        mock_process_message.return_value = 'Echo: Hello'

        await self.p2p_manager.handle_connection(mock_reader, mock_writer)

        mock_process_message.assert_called_once_with('Hello')
        mock_writer.write.assert_called_once_with(b'Echo: Hello\n')

    async def test_send_message_to_peer(self):
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        self.p2p_manager.connected_peers['peer1'] = (mock_reader, mock_writer)

        result = self.p2p_manager.send_message_to_peer('peer1', 'Test message')
        self.assertTrue(result)
        mock_writer.write.assert_called_once_with(b'Test message\n')

    @patch('src.p2p_manager.Config', {'P2P_PORT': 7175, 'KNOWN_PEERS': ['peer1:7176']})
    @patch.object(P2PManager, 'start')
    def test_create_p2p_manager(self, mock_start):
        manager = create_p2p_manager()
        self.assertIsInstance(manager, P2PManager)
        self.assertEqual(manager.port, 7175)
        self.assertEqual(manager.known_peers, ['peer1:7176'])
        mock_start.assert_called_once()

if __name__ == '__main__':
    unittest.main()