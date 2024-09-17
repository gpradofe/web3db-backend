from flask import request, jsonify
from flask_restx import Resource, fields
from . import api, p2p_manager, query_engine
import asyncio

peers_ns = api.namespace('peers', description='Peer operations')
query_ns = api.namespace('query', description='Query operations')

peer_model = api.model('Peer', {
    'peer_addr': fields.String(required=True, description='Peer address to connect to')
})

query_model = api.model('Query', {
    'query': fields.String(required=True, description='SQL Query'),
    'hash': fields.String(description='IPFS Hash of the existing database state')
})

@peers_ns.route('/')
class PeersResource(Resource):
    def get(self):
        '''Get the list of connected peers'''
        return jsonify({"peers": p2p_manager.get_connected_peers()})

    @api.expect(peer_model)
    def post(self):
        '''Connect to a new peer'''
        peer_addr = request.json.get("peer_addr")
        if not peer_addr:
            return {"error": "peer_addr is required"}, 400
        
        success = asyncio.run(p2p_manager.connect_to_peer(peer_addr))
        if success:
            return {"message": "Connected to peer successfully"}
        else:
            return {"error": "Failed to connect to peer"}, 500

@query_ns.route('/')
class QueryResource(Resource):
    @api.expect(query_model)
    def post(self):
        '''Execute a query and return the results'''
        query = request.json.get("query")
        data_hash = request.json.get("hash")
        
        if not query:
            return {"error": "query is required"}, 400
        
        result = query_engine.execute_query(query, data_hash)
        return jsonify({"result": result})