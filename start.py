#!/usr/bin/env python3
"""
BlockTracker Startup Script
Easy launcher for the enhanced BlockTracker system
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import requests
        import networkx
        import pandas
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_config():
    """Check if configuration file exists"""
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  No .env file found")
        print("Creating .env file from template...")
        
        if Path('config.env.example').exists():
            with open('config.env.example', 'r') as f:
                template = f.read()
            
            with open('.env', 'w') as f:
                f.write(template)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your Etherscan API key")
            print("   Get your API key from: https://etherscan.io/apis")
            return False
        else:
            print("❌ No config template found")
            return False
    
    # Check if API key is configured
    with open('.env', 'r') as f:
        content = f.read()
        if 'YourEtherscanApiKeyHere' in content:
            print("⚠️  Please configure your Etherscan API key in .env file")
            return False
    
    print("✅ Configuration file is properly set up")
    return True

def start_web_interface():
    """Start the web interface"""
    print("🚀 Starting BlockTracker Web Interface...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")

def run_cli_command(command):
    """Run a CLI command"""
    print(f"🚀 Running BlockTracker CLI: {command}")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'blocktracker_cli.py'] + command.split(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")

def show_menu():
    """Show interactive menu"""
    while True:
        print("\n" + "="*60)
        print("           🚀 BlockTracker Enhanced - Main Menu")
        print("="*60)
        print("1. 🌐 Start Web Interface (Recommended)")
        print("2. 💻 Run CLI Command")
        print("3. 🔧 Check System Status")
        print("4. 📚 Show Help")
        print("5. 🚪 Exit")
        print("="*60)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            start_web_interface()
        elif choice == '2':
            print("\nAvailable CLI commands:")
            print("  -w ADDRESS    : Detect cryptocurrency type")
            print("  -t ADDRESS    : Track transactions")
            print("  -a ADDRESS    : Full analysis with end receiver detection")
            print("  -g ADDRESS    : Generate transaction flow graph")
            print("\nExample: -a 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6")
            command = input("Enter CLI command: ").strip()
            if command:
                run_cli_command(command)
        elif choice == '3':
            check_system_status()
        elif choice == '4':
            show_help()
        elif choice == '5':
            print("👋 Goodbye! Happy blockchain tracking!")
            break
        else:
            print("❌ Invalid option. Please select 1-5.")

def check_system_status():
    """Check overall system status"""
    print("\n🔧 System Status Check")
    print("-" * 30)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check configuration
    config_ok = check_config()
    
    # Check data directory
    data_dir = Path('data')
    if data_dir.exists():
        print(f"✅ Data directory exists: {data_dir}")
    else:
        print(f"📁 Data directory will be created when needed")
    
    # Overall status
    if deps_ok and config_ok:
        print("\n🎉 System is ready to use!")
    else:
        print("\n⚠️  System needs configuration before use")

def show_help():
    """Show help information"""
    print("\n📚 BlockTracker Enhanced - Help")
    print("="*40)
    print("\nThis enhanced version of BlockTracker provides:")
    print("• Multi-chain cryptocurrency support (ETH, BTC, TRX)")
    print("• End receiver detection with probability scoring")
    print("• Interactive web interface with visualizations")
    print("• Advanced command-line interface")
    print("• Transaction flow analysis and graphing")
    
    print("\n🌐 Web Interface Features:")
    print("• Beautiful, responsive dashboard")
    print("• Interactive transaction flow graphs")
    print("• Real-time blockchain data")
    print("• End receiver probability analysis")
    
    print("\n💻 CLI Features:")
    print("• Address currency detection")
    print("• Transaction tracking")
    print("• Comprehensive analysis")
    print("• Graph generation")
    
    print("\n🔑 Required Setup:")
    print("• Etherscan API key for Ethereum analysis")
    print("• Bitcoin and TRON APIs are free")
    print("• Python 3.8+ with required packages")
    
    print("\n📖 For detailed usage, see README_ENHANCED.md")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='BlockTracker Enhanced - Easy Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--web', action='store_true',
                       help='Start web interface directly')
    parser.add_argument('--cli', type=str, metavar='COMMAND',
                       help='Run CLI command directly (e.g., "-a ADDRESS")')
    parser.add_argument('--check', action='store_true',
                       help='Check system status and exit')
    parser.add_argument('--show-help', action='store_true',
                       help='Show help and exit')
    
    args = parser.parse_args()
    
    # Show banner
    print("🚀 BlockTracker Enhanced - Cryptocurrency Transaction Analyzer")
    print("="*70)
    
    # Handle direct command execution
    if args.web:
        start_web_interface()
        return
    elif args.cli:
        run_cli_command(args.cli)
        return
    elif args.check:
        check_system_status()
        return
    elif args.show_help:
        show_help()
        return
    
    # Check system status first
    print("🔧 Checking system status...")
    deps_ok = check_dependencies()
    config_ok = check_config()
    
    if not deps_ok:
        print("\n❌ Please install dependencies first:")
        print("   pip install -r requirements.txt")
        return
    
    # Show interactive menu
    show_menu()

if __name__ == '__main__':
    main() 