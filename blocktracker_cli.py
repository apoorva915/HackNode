#!/usr/bin/env python3
"""
Enhanced BlockTracker CLI - Cryptocurrency Transaction Analyzer
Enhanced version of the original blocktracker.py with additional features
"""

import os
import argparse
import sys
from datetime import datetime
from core.blockchain_tracker import BlockchainTracker
from core.colors import *

def banner():
    """Display the BlockTracker banner"""
    print(yellow + "                                                        ,----,")
    print("                                                      ,/   .`|")
    print("    ,---,.   ,--,                            ,-.    ,`   .'  :                                 ,-.")
    print("  ,'  .'  \,--.'|                        ,--/ /|  ;    ;     /                             ,--/ /|")
    print(",---.' .' ||  | :     ,---.            ,--. :/ |.'___,/    ,' __  ,-.                    ,--. :/ |             __  ,-.")
    print("|   |  |: |:  : '    '   ,'\           :  : ' / |    :     |,' ,'/ /|                    :  : ' /            ,' ,'/ /|")
    print(":   :  :  /|  ' |   /   /   |   ,---.  |  '  /  ;    |.';  ;'  | |' | ,--.--.     ,---.  |  '  /      ,---.  '  | |' |")
    print(":   |    ; '  | |  .   ; ,. :  /     \ '  |  :  `----'  |  ||  |   ,'/       \   /     \ '  |  :     /     \ |  |   ,'")
    print("|   :     \|  | :  '   | |: : /    / ' |  |   \     '   :  ;'  :  / .--.  .-. | /    / ' |  |   \   /    /  |'  :  /")
    print("|   |   . |'  : |__'   | .; :.    ' /  '  : |. \    |   |  '|  | '   \__\/: . ..    ' /  '  : |. \ .    ' / ||  | '")
    print("'   :  '; ||  | '.'|   :    |'   ; :__ |  | ' \ \   '   :  |;  : |   ,' .--.; |'   ; :__ |  | ' \ \'   ;   /|;  : |")
    print("|   |  | ; ;  :    ;\   \  / '   | '.'|'  : |--'    ;   |.' |  , ;  /  /  ,.  |'   | '.'|'  : |--' '   |  / ||  , ;")
    print("|   :   /  |  ,   /  `----'  |   :    :;  |,'       '---'    ---'  ;  :   .'   \   :    :;  ,,'    |   :    | ---'")
    print("|   | ,'    ---`-'            \   \  / '--'                        |  ,     .-./\   \  / '--'       \   \  /")
    print("`----'                         `----'                               `--`---'     `----'              `----'\n")
    message()

def message():
    """Display author information"""
    print(f"""{red}   Enhanced Blockchain Transaction Tracker & End Receiver Analyzer       {green}°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸{red}
    ~ Enhanced by AI Assistant \ Python program \ {sys.platform}             {white}°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸{red}
     - Based on original by Keany Vy KHUN        {green}°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸{red}
      # Enhanced with multi-chain support & end receiver detection         {white}°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸{red}
       ^ Web interface available at http://localhost:5000                       {green}°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸{red}
    """)

def help():
    """Display help information"""
    print(f"""
     -------------------------------------------------------------          {white}E{red}n{white}h{red}a{white}n{red}c{white}e{red}d {white}B{red}l{white}o{red}c{white}k{red}T{white}r{red}a{white}c{red}k{white}e{red}r{red} !
    |  usage: blocktracker_cli.py [-h] [-w WHATADDRESS] [-t TRACK] [-a ANALYZE] [-g GRAPH] |               {white}__...--~~~~~-._   _.-~~~~~--...__{red}
    |                                                             |             {white}//               `V'               \\{red}
    |  optional arguments:                                        |            {white}//                 |                 \\{red}
    |  -h, --help            show this help message and exit      |           {white}//__...--~~~~~~-._  |  _.-~~~~~~--...__\\{red}
    |  -w WHATADDRESS, --whataddress WHATADDRESS                  |          {white}//__.....----~~~~._\ | /_.~~~~----.....__\\{red}
    |  Get type of wallet address                                 |         {white}====================\\|//===================={red}
    |  -t TRACK, --track TRACK                                    |                         {green}Enhanced `---`{red}
    |  Get all transactions from an address                       |
    |  -a ANALYZE, --analyze ANALYZE                             |
    |  Full transaction analysis with end receiver detection      |
    |  -g GRAPH, --graph GRAPH                                   |
    |  Generate transaction flow graph                            |
     -------------------------------------------------------------""")

def whataddress(addresses):
    """Detect cryptocurrency type from addresses"""
    tracker = BlockchainTracker()
    
    for i, address in enumerate(addresses):
        print(f"\nAddress #{i+1}: {address}")
        print("-" * 50)
        
        currency = tracker.detect_currency(address)
        if currency != 'UNKNOWN':
            print(f"Detected: {currency}")
        else:
            print("Unknown or unsupported address format")
        
        # Try to get additional info if it's a supported currency
        if currency in ['ETH', 'BTC', 'TRX']:
            print(f"Status: Supported for full analysis")
        else:
            print(f"Status: Basic support only")

def track_transactions(addresses):
    """Track transactions for addresses (enhanced version)"""
    tracker = BlockchainTracker()
    
    for i, address in enumerate(addresses):
        print(f"\nAddress #{i+1}: {address}")
        print("=" * 60)
        
        # Detect currency
        currency = tracker.detect_currency(address)
        print(f"Currency: {currency}")
        
        if currency not in ['ETH', 'BTC', 'TRX']:
            print(f"Warning: {currency} not fully supported for transaction tracking")
            continue
        
        # Analyze transaction flow
        try:
            result = tracker.analyze_transaction_flow(address, currency)
            
            if 'error' in result:
                print(f"Error: {result['error']}")
                continue
            
            # Display summary
            print(f"\nTransaction Summary:")
            print(f"  Total Transactions: {result['total_transactions']}")
            print(f"  Incoming: {result['incoming_transactions']}")
            print(f"  Outgoing: {result['outgoing_transactions']}")
            print(f"  Total Volume: {result['total_volume']:.6f} {currency}")
            
            # Display end receivers
            if result['end_receivers']:
                print(f"\nPotential End Receivers (Top 5):")
                for j, (receiver, probability) in enumerate(result['end_receivers'][:5]):
                    prob_percent = probability * 100
                    print(f"  {j+1}. {receiver} (Probability: {prob_percent:.1f}%)")
            
            # Display recent transactions
            if result['transactions']:
                print(f"\nRecent Transactions (Last 10):")
                for j, tx in enumerate(result['transactions'][-10:]):
                    print(f"  {j+1}. {tx.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"     From: {tx.from_address}")
                    print(f"     To: {tx.to_address}")
                    print(f"     Amount: {tx.amount:.6f} {tx.currency}")
                    print(f"     Hash: {tx.tx_hash}")
                    print()
            
        except Exception as e:
            print(f"Error analyzing address: {e}")

def analyze_address(addresses):
    """Full analysis with end receiver detection"""
    tracker = BlockchainTracker()
    
    for i, address in enumerate(addresses):
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE ANALYSIS - Address #{i+1}: {address}")
        print(f"{'='*80}")
        
        # Detect currency
        currency = tracker.detect_currency(address)
        print(f"Currency: {currency}")
        
        if currency not in ['ETH', 'BTC', 'TRX']:
            print(f"Warning: {currency} not fully supported for analysis")
            continue
        
        try:
            # Full analysis
            result = tracker.analyze_transaction_flow(address, currency)
            
            if 'error' in result:
                print(f"Error: {result['error']}")
                continue
            
            # Detailed statistics
            print(f"\n📊 TRANSACTION STATISTICS")
            print(f"  Total Transactions: {result['total_transactions']}")
            print(f"  Incoming Transactions: {result['incoming_transactions']}")
            print(f"  Outgoing Transactions: {result['outgoing_transactions']}")
            print(f"  Total Volume: {result['total_volume']:.6f} {currency}")
            
            # End receiver analysis
            if result['end_receivers']:
                print(f"\n🎯 END RECEIVER ANALYSIS")
                print(f"  Found {len(result['end_receivers'])} potential end receivers:")
                
                for j, (receiver, probability) in enumerate(result['end_receivers']):
                    prob_percent = probability * 100
                    confidence = "High" if prob_percent > 70 else "Medium" if prob_percent > 40 else "Low"
                    
                    print(f"  {j+1}. {receiver}")
                    print(f"     Probability: {prob_percent:.1f}% ({confidence} confidence)")
                    
                    # Add visual probability bar
                    bar_length = 20
                    filled_length = int((prob_percent / 100) * bar_length)
                    bar = "█" * filled_length + "░" * (bar_length - filled_length)
                    print(f"     Confidence: [{bar}] {prob_percent:.1f}%")
                    print()
            
            # Transaction flow analysis
            graph = result['transaction_tree']
            print(f"\n🔄 TRANSACTION FLOW ANALYSIS")
            print(f"  Nodes in graph: {graph.number_of_nodes()}")
            print(f"  Edges in graph: {graph.number_of_edges()}")
            
            # Find paths to end receivers
            if result['end_receivers']:
                print(f"  Path analysis to top end receiver:")
                top_receiver = result['end_receivers'][0][0]
                
                try:
                    # Find shortest path
                    if nx.has_path(graph, address, top_receiver):
                        path = nx.shortest_path(graph, address, top_receiver)
                        print(f"    Path length: {len(path) - 1} hops")
                        print(f"    Path: {' -> '.join([p[:10] + '...' for p in path])}")
                    else:
                        print(f"    No direct path found to {top_receiver[:10]}...")
                except:
                    print(f"    Path analysis not available")
            
        except Exception as e:
            print(f"Error during analysis: {e}")

def generate_graph(addresses):
    """Generate transaction flow graphs"""
    tracker = BlockchainTracker()
    
    for i, address in enumerate(addresses):
        print(f"\nGenerating graph for Address #{i+1}: {address}")
        
        try:
            result = tracker.analyze_transaction_flow(address)
            
            if 'error' in result:
                print(f"Error: {result['error']}")
                continue
            
            graph = result['transaction_tree']
            
            print(f"Graph generated successfully!")
            print(f"  Nodes: {graph.number_of_nodes()}")
            print(f"  Edges: {graph.number_of_edges()}")
            print(f"  Graph saved to: data/{address}_graph.json")
            
            # Save graph data for visualization
            import json
            from datetime import datetime
            
            graph_data = {
                'address': address,
                'currency': result['currency'],
                'timestamp': datetime.now().isoformat(),
                'nodes': [],
                'edges': []
            }
            
            for node in graph.nodes():
                node_data = graph.nodes[node]
                graph_data['nodes'].append({
                    'id': node,
                    'currency': node_data.get('currency', 'Unknown'),
                    'first_seen': node_data.get('first_seen', '').isoformat() if node_data.get('first_seen') else '',
                    'last_seen': node_data.get('last_seen', '').isoformat() if node_data.get('last_seen') else ''
                })
            
            for edge in graph.edges(data=True):
                graph_data['edges'].append({
                    'source': edge[0],
                    'target': edge[1],
                    'tx_hash': edge[2].get('tx_hash', ''),
                    'amount': edge[2].get('amount', 0),
                    'timestamp': edge[2].get('timestamp', '').isoformat() if edge[2].get('timestamp') else '',
                    'currency': edge[2].get('currency', 'Unknown')
                })
            
            # Ensure data directory exists
            if not os.path.exists('data'):
                os.makedirs('data')
            
            # Save graph data
            with open(f'data/{address}_graph.json', 'w') as f:
                json.dump(graph_data, f, indent=2)
                
        except Exception as e:
            print(f"Error generating graph: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Enhanced BlockTracker - Cryptocurrency Transaction Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -w 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
  %(prog)s -t 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
  %(prog)s -a 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
  %(prog)s -g 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
        """
    )
    
    parser.add_argument('-w', '--whataddress', 
                       help='Detect cryptocurrency type from wallet address(es)', 
                       nargs='+', dest='whataddress')
    parser.add_argument('-t', '--track', 
                       help='Track transactions from address(es)', 
                       nargs='+', dest='track')
    parser.add_argument('-a', '--analyze', 
                       help='Full analysis with end receiver detection', 
                       nargs='+', dest='analyze')
    parser.add_argument('-g', '--graph', 
                       help='Generate transaction flow graph', 
                       nargs='+', dest='graph')
    
    args = parser.parse_args()
    
    # Show banner if no arguments
    if not any([args.whataddress, args.track, args.analyze, args.graph]):
        banner()
        help()
        return
    
    # Process arguments
    if args.whataddress:
        whataddress(args.whataddress)
    
    if args.track:
        track_transactions(args.track)
    
    if args.analyze:
        analyze_address(args.analyze)
    
    if args.graph:
        generate_graph(args.graph)

if __name__ == '__main__':
    main() 