from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from datetime import datetime
from core.blockchain_tracker import BlockchainTracker
import networkx as nx

app = Flask(__name__)
CORS(app)

# Initialize blockchain tracker
tracker = BlockchainTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_address():
    """Analyze a cryptocurrency address and return transaction flow"""
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        # Analyze the address
        result = tracker.analyze_transaction_flow(address)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Convert datetime objects to strings for JSON serialization
        serializable_result = {
            'address': result['address'],
            'currency': result['currency'],
            'total_transactions': result['total_transactions'],
            'incoming_transactions': result['incoming_transactions'],
            'outgoing_transactions': result['outgoing_transactions'],
            'total_volume': result['total_volume'],
            'end_receivers': result['end_receivers'],
            'transactions': []
        }
        
        # Serialize transactions
        for tx in result['transactions']:
            serializable_tx = {
                'tx_hash': tx.tx_hash,
                'from_address': tx.from_address,
                'to_address': tx.to_address,
                'timestamp': tx.timestamp.isoformat(),
                'amount': tx.amount,
                'currency': tx.currency,
                'block_number': tx.block_number
            }
            serializable_result['transactions'].append(serializable_tx)
        
        return jsonify(serializable_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/currency-detect', methods=['POST'])
def detect_currency():
    """Detect cryptocurrency type from address"""
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        currency = tracker.detect_currency(address)
        return jsonify({'address': address, 'currency': currency})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transaction-graph', methods=['POST'])
def get_transaction_graph():
    """Get transaction graph data for visualization"""
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        if not address:
            return jsonify({'error': 'Address is required'}), 400
        
        # Analyze the address
        result = tracker.analyze_transaction_flow(address)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Convert NetworkX graph to serializable format
        graph = result['transaction_tree']
        
        nodes = []
        edges = []
        
        for node in graph.nodes():
            node_data = graph.nodes[node]
            nodes.append({
                'id': node,
                'currency': node_data.get('currency', 'Unknown'),
                'first_seen': node_data.get('first_seen', '').isoformat() if node_data.get('first_seen') else '',
                'last_seen': node_data.get('last_seen', '').isoformat() if node_data.get('last_seen') else ''
            })
        
        for edge in graph.edges(data=True):
            edges.append({
                'source': edge[0],
                'target': edge[1],
                'tx_hash': edge[2].get('tx_hash', ''),
                'amount': edge[2].get('amount', 0),
                'timestamp': edge[2].get('timestamp', '').isoformat() if edge[2].get('timestamp') else '',
                'currency': edge[2].get('currency', 'Unknown')
            })
        
        return jsonify({
            'nodes': nodes,
            'edges': edges,
            'address': address,
            'currency': result['currency']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 