from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from datetime import datetime
from core.blockchain_tracker import BlockchainTracker
from core.logger import get_logger
import networkx as nx
import time

app = Flask(__name__)
CORS(app)

# Initialize logger
logger = get_logger("FlaskApp")

# Initialize blockchain tracker
logger.info("Initializing Flask application")
tracker = BlockchainTracker()
logger.info("Flask application initialized successfully")

@app.route('/')
def index():
    logger.info("Homepage accessed")
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_address():
    """Analyze a cryptocurrency address and return transaction flow"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        logger.info(f"Address analysis requested: {address[:10]}...")
        
        if not address:
            logger.warning("Address analysis failed: No address provided")
            return jsonify({'error': 'Address is required'}), 400
        
        # Analyze the address
        logger.info(f"Starting analysis for address: {address[:10]}...")
        result = tracker.analyze_transaction_flow(address)
        
        if 'error' in result:
            logger.error(f"Address analysis failed: {result['error']}", 
                        context={'address': address, 'error': result['error']})
            return jsonify(result), 400
        
        # Log successful analysis
        analysis_time = time.time() - start_time
        logger.log_transaction_analysis(
            address=address,
            currency=result['currency'],
            transaction_count=result['total_transactions'],
            end_receivers=len(result['end_receivers']),
            analysis_time=analysis_time,
            success=True
        )
        
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
        
        logger.info(f"Address analysis completed successfully: {address[:10]}... | "
                   f"Transactions: {result['total_transactions']} | Time: {analysis_time:.3f}s")
        
        return jsonify(serializable_result)
        
    except Exception as e:
        analysis_time = time.time() - start_time
        logger.log_error(e, context={
            'address': address if 'address' in locals() else 'unknown',
            'analysis_time': analysis_time,
            'endpoint': '/api/analyze'
        })
        return jsonify({'error': str(e)}), 500

@app.route('/api/currency-detect', methods=['POST'])
def detect_currency():
    """Detect cryptocurrency type from address"""
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        logger.info(f"Currency detection requested: {address[:10]}...")
        
        if not address:
            logger.warning("Currency detection failed: No address provided")
            return jsonify({'error': 'Address is required'}), 400
        
        currency = tracker.detect_currency(address)
        logger.info(f"Currency detection completed: {address[:10]}... -> {currency}")
        
        return jsonify({'address': address, 'currency': currency})
        
    except Exception as e:
        logger.log_error(e, context={
            'address': address if 'address' in locals() else 'unknown',
            'endpoint': '/api/currency-detect'
        })
        return jsonify({'error': str(e)}), 500

@app.route('/api/transaction-graph', methods=['POST'])
def get_transaction_graph():
    """Get transaction graph data for visualization"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        address = data.get('address', '').strip()
        
        logger.info(f"Transaction graph requested for address: {address[:10]}...")
        
        if not address:
            logger.warning("Transaction graph failed: No address provided")
            return jsonify({'error': 'Address is required'}), 400
        
        # Analyze the address
        logger.info(f"Starting graph analysis for address: {address[:10]}...")
        result = tracker.analyze_transaction_flow(address)
        
        if 'error' in result:
            logger.error(f"Transaction graph analysis failed: {result['error']}", 
                        context={'address': address, 'error': result['error']})
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
        
        graph_time = time.time() - start_time
        logger.info(f"Transaction graph generated successfully: {address[:10]}... | "
                   f"Nodes: {len(nodes)} | Edges: {len(edges)} | Time: {graph_time:.3f}s")
        
        return jsonify({
            'nodes': nodes,
            'edges': edges,
            'address': address,
            'currency': result['currency']
        })
        
    except Exception as e:
        graph_time = time.time() - start_time
        logger.log_error(e, context={
            'address': address if 'address' in locals() else 'unknown',
            'graph_time': graph_time,
            'endpoint': '/api/transaction-graph'
        })
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    logger.info("Starting Flask server")
    try:
        logger.log_startup({
            'host': '0.0.0.0',
            'port': 5000,
            'debug': True
        })
    except Exception as e:
        logger.error(f"Error in startup logging: {e}")
    
    logger.info("Flask server starting on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 