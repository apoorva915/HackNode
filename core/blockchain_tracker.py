import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import networkx as nx
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from .logger import get_logger

load_dotenv()

# Initialize logger
logger = get_logger("BlockchainTracker")

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
        logger.info("Initializing BlockchainTracker")
        
        self.etherscan_api_key = os.getenv('ETHERSCAN_API_KEY', '')
        self.bitcoin_api_url = "https://blockstream.info/api"
        self.tron_api_url = "https://api.trongrid.io"
        
        # Log configuration
        config_info = {
            'etherscan_api_key_configured': bool(self.etherscan_api_key),
            'bitcoin_api_url': self.bitcoin_api_url,
            'tron_api_url': self.tron_api_url
        }
        logger.info(f"BlockchainTracker configuration: {config_info}")
        
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'BlockTracker/1.0'})
        
        logger.info("BlockchainTracker initialized successfully")
        
    def detect_currency(self, address: str) -> str:
        """Detect cryptocurrency type from address format"""
        logger.info(f"Detecting currency for address: {address[:10]}...")
        
        address_lower = address.lower()
        detected_currency = 'UNKNOWN'
        
        if address_lower.startswith('0x'):
            detected_currency = 'ETH'
        elif address_lower.startswith('bc1') or address_lower.startswith('1') or address_lower.startswith('3'):
            detected_currency = 'BTC'
        elif address_lower.startswith('t') and len(address) == 34:
            detected_currency = 'TRX'
        elif address_lower.startswith('addr'):
            detected_currency = 'ADA'
        elif address_lower.startswith('cosmos'):
            detected_currency = 'ATOM'
        elif address_lower.startswith('r'):
            detected_currency = 'XRP'
        elif address_lower.startswith('g'):
            detected_currency = 'XLM'
        
        logger.info(f"Currency detection result: {address[:10]}... -> {detected_currency}")
        return detected_currency
    
    def get_ethereum_transactions(self, address: str, max_transactions: int = 1000) -> List[Transaction]:
        """Fetch Ethereum transactions from Etherscan"""
        start_time = time.time()
        logger.info(f"Fetching Ethereum transactions for address: {address[:10]}... | Max: {max_transactions}")
        
        if not self.etherscan_api_key:
            logger.warning("No Etherscan API key provided. Using demo mode.")
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
            
            logger.info(f"Making Etherscan API request: {url} | Params: {params}")
            
            response = self.session.get(url, params=params)
            response_time = time.time() - start_time
            
            # Log API call details
            logger.log_api_call(
                method="GET",
                url=url,
                status_code=response.status_code,
                response_time=response_time,
                request_data=params,
                response_data={"status": response.status_code, "content_length": len(response.content)}
            )
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"Etherscan API response received: Status={data.get('status')} | Message={data.get('message', 'N/A')}")
            
            if data['status'] != '1':
                error_msg = data.get('message', 'Unknown error')
                logger.error(f"Etherscan API error: {error_msg}")
                return []
            
            transactions = []
            successful_parses = 0
            failed_parses = 0
            
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
                    successful_parses += 1
                    
                except Exception as e:
                    logger.error(f"Error parsing transaction {tx.get('hash', 'unknown')}: {e}", 
                               context={'tx_data': tx, 'address': address})
                    failed_parses += 1
                    continue
            
            total_time = time.time() - start_time
            logger.info(f"Ethereum transaction fetch completed: {len(transactions)} transactions | "
                       f"Successful parses: {successful_parses} | Failed parses: {failed_parses} | "
                       f"Total time: {total_time:.3f}s")
            
            return transactions
            
        except Exception as e:
            total_time = time.time() - start_time
            logger.log_error(e, context={
                'address': address,
                'max_transactions': max_transactions,
                'api_key_configured': bool(self.etherscan_api_key),
                'total_time': total_time
            })
            return []
    
    def get_bitcoin_transactions(self, address: str, max_transactions: int = 1000) -> List[Transaction]:
        """Fetch Bitcoin transactions from Blockstream API"""
        start_time = time.time()
        logger.info(f"Fetching Bitcoin transactions for address: {address[:10]}... | Max: {max_transactions}")
        
        try:
            # Get address info
            url = f"{self.bitcoin_api_url}/address/{address}"
            logger.info(f"Making Bitcoin API request: {url}")
            
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            # Log API call details
            logger.log_api_call(
                method="GET",
                url=url,
                status_code=response.status_code,
                response_time=response_time,
                request_data={"address": address},
                response_data={"status": response.status_code, "content_length": len(response.content)}
            )
            
            response.raise_for_status()
            address_data = response.json()
            
            logger.info(f"Bitcoin API response received: Status={response.status_code} | "
                       f"Address data keys: {list(address_data.keys())}")
            
            transactions = []
            tx_count = address_data.get('chain_stats', {}).get('tx_count', 0)
            logger.info(f"Found {tx_count} total transactions for Bitcoin address")
            
            if not tx_count:
                logger.info("No transactions found for Bitcoin address")
                return []
                
            # Get recent transactions
            tx_list_url = f"{self.bitcoin_api_url}/address/{address}/txs"
            logger.info(f"Fetching transaction list from: {tx_list_url}")
            
            tx_response = self.session.get(tx_list_url)
            if tx_response.status_code != 200:
                logger.error(f"Failed to fetch Bitcoin transaction list: {tx_response.status_code}")
                return []
                
            tx_list = tx_response.json()
            logger.info(f"Retrieved {len(tx_list)} transactions from Bitcoin API")
            
            successful_parses = 0
            failed_parses = 0
            
            for tx in tx_list[:max_transactions]:
                if len(transactions) >= max_transactions:
                    break
                    
                try:
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
                        successful_parses += 1
                    else:
                        logger.debug(f"Skipping transaction {tx_hash}: missing block_time or tx_hash")
                        
                except Exception as e:
                    logger.error(f"Error parsing Bitcoin transaction {tx.get('txid', 'unknown')}: {e}",
                               context={'tx_data': tx, 'address': address})
                    failed_parses += 1
                    continue
            
            total_time = time.time() - start_time
            logger.info(f"Bitcoin transaction fetch completed: {len(transactions)} transactions | "
                       f"Successful parses: {successful_parses} | Failed parses: {failed_parses} | "
                       f"Total time: {total_time:.3f}s")
            
            return transactions
            
        except Exception as e:
            total_time = time.time() - start_time
            logger.log_error(e, context={
                'address': address,
                'max_transactions': max_transactions,
                'api_url': self.bitcoin_api_url,
                'total_time': total_time
            })
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
        logger.info(f"Building transaction tree from {len(transactions)} transactions")
        
        G = nx.DiGraph()
        nodes_added = 0
        edges_added = 0
        
        for i, tx in enumerate(transactions):
            try:
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
                
                nodes_added += 2  # from and to addresses
                edges_added += 1
                
                if (i + 1) % 100 == 0:  # Log progress every 100 transactions
                    logger.debug(f"Processed {i + 1}/{len(transactions)} transactions")
                    
            except Exception as e:
                logger.error(f"Error processing transaction {i}: {e}", 
                           context={'tx_index': i, 'tx_hash': tx.tx_hash})
                continue
        
        logger.info(f"Transaction tree built successfully: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G
    
    def find_end_receivers(self, graph: nx.DiGraph, start_address: str, max_depth: int = 5) -> List[Tuple[str, float]]:
        """Find potential end receivers with probability scores"""
        logger.info(f"Finding end receivers for address: {start_address[:10]}... | Max depth: {max_depth}")
        
        end_receivers = []
        visited = set()
        paths_explored = 0
        
        def dfs(node, depth, path_probability):
            nonlocal paths_explored
            if depth > max_depth or node in visited:
                return
            
            visited.add(node)
            paths_explored += 1
            
            # Check if this is an end receiver (no outgoing edges)
            successors = list(graph.successors(node))
            if not successors:
                end_receivers.append((node, path_probability))
                logger.debug(f"Found end receiver: {node[:10]}... | Depth: {depth} | Probability: {path_probability:.3f}")
                return
            
            # Continue traversing
            for successor in successors:
                edge_data = graph.get_edge_data(node, successor)
                if edge_data:
                    # Reduce probability with each hop
                    new_probability = path_probability * 0.8  # 20% reduction per hop
                    dfs(successor, depth + 1, new_probability)
        
        # Start DFS from the given address
        logger.info(f"Starting DFS traversal from: {start_address[:10]}...")
        dfs(start_address, 0, 1.0)
        
        # Sort by probability and return top candidates
        end_receivers.sort(key=lambda x: x[1], reverse=True)
        top_candidates = end_receivers[:10]  # Return top 10
        
        logger.info(f"End receiver detection completed: {len(end_receivers)} found, {len(top_candidates)} returned | "
                   f"Paths explored: {paths_explored} | Visited nodes: {len(visited)}")
        
        if top_candidates:
            logger.info(f"Top end receiver: {top_candidates[0][0][:10]}... | Probability: {top_candidates[0][1]:.3f}")
        
        return top_candidates
    
    def analyze_transaction_flow(self, address: str, currency: str = None) -> Dict:
        """Analyze transaction flow for a given address"""
        start_time = time.time()
        logger.info(f"Starting transaction flow analysis for address: {address[:10]}...")
        
        if not currency:
            logger.info(f"Auto-detecting currency for address: {address[:10]}...")
            currency = self.detect_currency(address)
            logger.info(f"Detected currency: {currency}")
        
        # Fetch transactions based on currency
        logger.info(f"Fetching transactions for {currency} address: {address[:10]}...")
        
        if currency == 'ETH':
            transactions = self.get_ethereum_transactions(address)
        elif currency == 'BTC':
            transactions = self.get_bitcoin_transactions(address)
        elif currency == 'TRX':
            transactions = self.get_tron_transactions(address)
        else:
            logger.warning(f"Unsupported currency: {currency} for address: {address[:10]}...")
            return {"error": f"Unsupported currency: {currency}"}
        
        if not transactions:
            logger.warning(f"No transactions found for address: {address[:10]}... | Currency: {currency}")
            return {"error": "No transactions found"}
        
        logger.info(f"Retrieved {len(transactions)} transactions for {currency} address: {address[:10]}...")
        
        # Build transaction tree
        logger.info(f"Building transaction tree for address: {address[:10]}...")
        tree_start_time = time.time()
        graph = self.build_transaction_tree(transactions)
        tree_time = time.time() - tree_start_time
        logger.info(f"Transaction tree built: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges | Time: {tree_time:.3f}s")
        
        # Find end receivers
        logger.info(f"Finding end receivers for address: {address[:10]}...")
        receiver_start_time = time.time()
        end_receivers = self.find_end_receivers(graph, address)
        receiver_time = time.time() - receiver_start_time
        logger.info(f"Found {len(end_receivers)} end receivers | Time: {receiver_time:.3f}s")
        
        # Calculate statistics
        total_incoming = sum(1 for tx in transactions if tx.to_address == address)
        total_outgoing = sum(1 for tx in transactions if tx.from_address == address)
        total_volume = sum(tx.amount for tx in transactions)
        
        total_time = time.time() - start_time
        
        logger.info(f"Transaction flow analysis completed: {address[:10]}... | "
                   f"Currency: {currency} | Transactions: {len(transactions)} | "
                   f"Incoming: {total_incoming} | Outgoing: {total_outgoing} | "
                   f"Volume: {total_volume:.6f} | End Receivers: {len(end_receivers)} | "
                   f"Total Time: {total_time:.3f}s")
        
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