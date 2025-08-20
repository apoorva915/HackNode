import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import networkx as nx
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Transaction:
    tx_hash: str
    from_address: str
    to_address: str
    timestamp: datetime
    amount: float
    currency: str
    block_number: int
    gas_price: Optional[float] = None
    gas_used: Optional[float] = None

@dataclass
class AddressInfo:
    address: str
    currency: str
    balance: float
    transaction_count: int
    first_seen: datetime
    last_seen: datetime

class BlockchainTracker:
    def __init__(self):
        self.etherscan_api_key = os.getenv('ETHERSCAN_API_KEY', '')
        self.bitcoin_api_url = "https://blockstream.info/api"
        self.tron_api_url = "https://api.trongrid.io"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'BlockTracker/1.0'})
        
    def detect_currency(self, address: str) -> str:
        """Detect cryptocurrency type from address format"""
        address_lower = address.lower()
        
        if address_lower.startswith('0x'):
            return 'ETH'
        elif address_lower.startswith('bc1') or address_lower.startswith('1') or address_lower.startswith('3'):
            return 'BTC'
        elif address_lower.startswith('t') and len(address) == 34:
            return 'TRX'
        elif address_lower.startswith('addr'):
            return 'ADA'
        elif address_lower.startswith('cosmos'):
            return 'ATOM'
        elif address_lower.startswith('r'):
            return 'XRP'
        elif address_lower.startswith('g'):
            return 'XLM'
        else:
            return 'UNKNOWN'
    
    def get_ethereum_transactions(self, address: str, max_transactions: int = 1000) -> List[Transaction]:
        """Fetch Ethereum transactions from Etherscan"""
        if not self.etherscan_api_key:
            print("Warning: No Etherscan API key provided. Using demo mode.")
            return []
        
        try:
            url = f"https://api.etherscan.io/api"
            params = {
                'module': 'account',
                'action': 'txlist',
                'address': address,
                'startblock': 0,
                'endblock': 99999999,
                'sort': 'asc',
                'apikey': self.etherscan_api_key
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != '1':
                print(f"Etherscan API error: {data.get('message', 'Unknown error')}")
                return []
            
            transactions = []
            for tx in data['result'][:max_transactions]:
                try:
                    amount_eth = float(tx['value']) / 10**18  # Convert from wei to ETH
                    timestamp = datetime.fromtimestamp(int(tx['timeStamp']))
                    
                    transaction = Transaction(
                        tx_hash=tx['hash'],
                        from_address=tx['from'],
                        to_address=tx['to'],
                        timestamp=timestamp,
                        amount=amount_eth,
                        currency='ETH',
                        block_number=int(tx['blockNumber']),
                        gas_price=float(tx['gasPrice']) / 10**9 if tx['gasPrice'] else None,
                        gas_used=float(tx['gasUsed']) if tx['gasUsed'] else None
                    )
                    transactions.append(transaction)
                except Exception as e:
                    print(f"Error parsing transaction {tx['hash']}: {e}")
                    continue
            
            return transactions
            
        except Exception as e:
            print(f"Error fetching Ethereum transactions: {e}")
            return []
    
    def get_bitcoin_transactions(self, address: str, max_transactions: int = 1000) -> List[Transaction]:
        """Fetch Bitcoin transactions from Blockstream API"""
        try:
            # Get address info
            url = f"{self.bitcoin_api_url}/address/{address}"
            response = self.session.get(url)
            response.raise_for_status()
            address_data = response.json()
            
            transactions = []
            tx_count = address_data.get('chain_stats', {}).get('tx_count', 0)
            if not tx_count:
                return []
                
            # Get recent transactions
            tx_list_url = f"{self.bitcoin_api_url}/address/{address}/txs"
            tx_response = self.session.get(tx_list_url)
            if tx_response.status_code != 200:
                return []
                
            tx_list = tx_response.json()
            for tx in tx_list[:max_transactions]:
                if len(transactions) >= max_transactions:
                    break
                    
                # Parse transaction data
                tx_hash = tx.get('txid', '')
                block_time = tx.get('status', {}).get('block_time', 0)
                block_height = tx.get('status', {}).get('block_height', 0)
                
                if block_time and tx_hash:
                    # For Bitcoin, we'll create a simplified transaction
                    # In a real implementation, you'd parse inputs/outputs more carefully
                    transaction = Transaction(
                        tx_hash=tx_hash,
                        from_address=address,
                        to_address='',  # Would be parsed from outputs
                        timestamp=datetime.fromtimestamp(block_time),
                        amount=0.001,  # Placeholder amount
                        currency='BTC',
                        block_number=block_height
                    )
                    transactions.append(transaction)
            
            return transactions
            
        except Exception as e:
            print(f"Error fetching Bitcoin transactions: {e}")
            return []
    
    def get_tron_transactions(self, address: str, max_transactions: int = 1000) -> List[Transaction]:
        """Fetch TRON transactions from TronGrid API"""
        try:
            url = f"{self.tron_api_url}/v1/accounts/{address}/transactions"
            params = {'limit': max_transactions}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            transactions = []
            for tx in data.get('data', []):
                try:
                    if tx.get('type') == 'Transfer':
                        amount_trx = float(tx.get('value', 0)) / 10**6  # Convert from sun to TRX
                        
                        transaction = Transaction(
                            tx_hash=tx['txID'],
                            from_address=tx.get('from', ''),
                            to_address=tx.get('to', ''),
                            timestamp=datetime.fromtimestamp(tx['block_timestamp'] / 1000),
                            amount=amount_trx,
                            currency='TRX',
                            block_number=tx.get('block', 0)
                        )
                        transactions.append(transaction)
                except Exception as e:
                    print(f"Error parsing TRON transaction {tx.get('txID', 'unknown')}: {e}")
                    continue
            
            return transactions
            
        except Exception as e:
            print(f"Error fetching TRON transactions: {e}")
            return []
    
    def build_transaction_tree(self, transactions: List[Transaction]) -> nx.DiGraph:
        """Build a directed graph representing the transaction flow"""
        G = nx.DiGraph()
        
        for tx in transactions:
            # Add nodes
            G.add_node(tx.from_address, 
                      currency=tx.currency, 
                      first_seen=tx.timestamp,
                      last_seen=tx.timestamp)
            G.add_node(tx.to_address, 
                      currency=tx.currency,
                      first_seen=tx.timestamp,
                      last_seen=tx.timestamp)
            
            # Add edge
            G.add_edge(tx.from_address, tx.to_address, 
                      tx_hash=tx.tx_hash,
                      amount=tx.amount,
                      timestamp=tx.timestamp,
                      currency=tx.currency)
        
        return G
    
    def find_end_receivers(self, graph: nx.DiGraph, start_address: str, max_depth: int = 5) -> List[Tuple[str, float]]:
        """Find potential end receivers with probability scores"""
        end_receivers = []
        visited = set()
        
        def dfs(node, depth, path_probability):
            if depth > max_depth or node in visited:
                return
            
            visited.add(node)
            
            # Check if this is an end receiver (no outgoing edges)
            successors = list(graph.successors(node))
            if not successors:
                end_receivers.append((node, path_probability))
                return
            
            # Continue traversing
            for successor in successors:
                edge_data = graph.get_edge_data(node, successor)
                if edge_data:
                    # Reduce probability with each hop
                    new_probability = path_probability * 0.8  # 20% reduction per hop
                    dfs(successor, depth + 1, new_probability)
        
        # Start DFS from the given address
        dfs(start_address, 0, 1.0)
        
        # Sort by probability and return top candidates
        end_receivers.sort(key=lambda x: x[1], reverse=True)
        return end_receivers[:10]  # Return top 10
    
    def analyze_transaction_flow(self, address: str, currency: str = None) -> Dict:
        """Analyze transaction flow for a given address"""
        if not currency:
            currency = self.detect_currency(address)
        
        # Fetch transactions based on currency
        if currency == 'ETH':
            transactions = self.get_ethereum_transactions(address)
        elif currency == 'BTC':
            transactions = self.get_bitcoin_transactions(address)
        elif currency == 'TRX':
            transactions = self.get_tron_transactions(address)
        else:
            return {"error": f"Unsupported currency: {currency}"}
        
        if not transactions:
            return {"error": "No transactions found"}
        
        # Build transaction tree
        graph = self.build_transaction_tree(transactions)
        
        # Find end receivers
        end_receivers = self.find_end_receivers(graph, address)
        
        # Calculate statistics
        total_incoming = sum(1 for tx in transactions if tx.to_address == address)
        total_outgoing = sum(1 for tx in transactions if tx.from_address == address)
        total_volume = sum(tx.amount for tx in transactions)
        
        return {
            "address": address,
            "currency": currency,
            "total_transactions": len(transactions),
            "incoming_transactions": total_incoming,
            "outgoing_transactions": total_outgoing,
            "total_volume": total_volume,
            "end_receivers": end_receivers,
            "transaction_tree": graph,
            "transactions": transactions
        } 