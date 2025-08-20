# Enhanced BlockTracker - Cryptocurrency Transaction Analyzer

A comprehensive software solution to identify the end receiver of cryptocurrency transactions with advanced blockchain analysis capabilities.

## 🚀 What's New in the Enhanced Version

This enhanced version of BlockTracker goes far beyond the original project, providing:

- **Multi-Chain Support**: Ethereum, Bitcoin, TRON, and more
- **End Receiver Detection**: Advanced algorithms to trace fund flows to final destinations
- **Transaction Tree Building**: Visual representation of transaction networks
- **Modern Web Interface**: Beautiful, responsive dashboard with interactive visualizations
- **Probability Scoring**: Confidence levels for end receiver predictions
- **API Backend**: RESTful API for integration with other systems
- **Enhanced CLI**: Command-line interface with new analysis features

## 🎯 Key Features

### 1. End Receiver Detection
- **Fund Flow Tracing**: Follow cryptocurrency transactions through multiple addresses
- **Probability Analysis**: Calculate confidence scores for potential end receivers
- **Path Analysis**: Identify transaction paths and hop counts
- **Mixing Detection**: Recognize when funds are being mixed or laundered

### 2. Multi-Chain Support
- **Ethereum (ETH)**: Full transaction analysis via Etherscan API
- **Bitcoin (BTC)**: Transaction tracking via Blockstream API
- **TRON (TRX)**: Transaction analysis via TronGrid API
- **Extensible**: Easy to add support for more cryptocurrencies

### 3. Advanced Visualizations
- **Interactive Network Graphs**: Visualize transaction flows with vis.js
- **Transaction Trees**: Hierarchical view of fund movements
- **Real-time Updates**: Live data from blockchain APIs
- **Responsive Design**: Works on desktop, tablet, and mobile

### 4. Dual Interface
- **Web Dashboard**: Modern, user-friendly web interface
- **Command Line**: Powerful CLI for automation and scripting

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/blocktracker.git
cd blocktracker
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys
```bash
# Copy the example configuration
cp config.env.example .env

# Edit .env file and add your API keys
# Get Etherscan API key from: https://etherscan.io/apis
ETHERSCAN_API_KEY=YourEtherscanApiKeyHere
```

### Step 4: Run the Application

#### Option A: Web Interface (Recommended)
```bash
python app.py
```
Then open your browser to: http://localhost:5000

#### Option B: Command Line Interface
```bash
python blocktracker_cli.py -h
```

## 📖 Usage Guide

### Web Interface

1. **Open the Dashboard**: Navigate to http://localhost:5000
2. **Enter Address**: Input any cryptocurrency address in the search bar
3. **Analyze**: Click "Analyze" to start the analysis
4. **View Results**: Explore the comprehensive analysis results:
   - Transaction statistics
   - End receiver predictions with confidence scores
   - Interactive transaction flow graph
   - Detailed transaction history

### Command Line Interface

#### Basic Address Detection
```bash
# Detect cryptocurrency type from address
python blocktracker_cli.py -w 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
```

#### Transaction Tracking
```bash
# Track transactions from an address
python blocktracker_cli.py -t 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
```

#### Full Analysis
```bash
# Comprehensive analysis with end receiver detection
python blocktracker_cli.py -a 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
```

#### Generate Graphs
```bash
# Create transaction flow graphs
python blocktracker_cli.py -g 0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6
```

#### Multiple Addresses
```bash
# Analyze multiple addresses at once
python blocktracker_cli.py -a address1 address2 address3
```

## 🔧 API Endpoints

The web interface is backed by a RESTful API:

### Analyze Address
```http
POST /api/analyze
Content-Type: application/json

{
  "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
}
```

### Detect Currency
```http
POST /api/currency-detect
Content-Type: application/json

{
  "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
}
```

### Get Transaction Graph
```http
POST /api/transaction-graph
Content-Type: application/json

{
  "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
}
```

### Health Check
```http
GET /api/health
```

## 📊 Understanding the Results

### End Receiver Analysis
The system identifies potential end receivers with probability scores:

- **High Confidence (70%+)**: Strong evidence this is the final destination
- **Medium Confidence (40-70%)**: Moderate evidence, worth investigating
- **Low Confidence (<40%)**: Weak evidence, may be intermediate address

### Transaction Flow Graph
- **Nodes**: Represent wallet addresses
- **Edges**: Show transaction flows with amounts and timestamps
- **Colors**: Different colors for different cryptocurrencies
- **Interactive**: Zoom, pan, and hover for details

### Statistics Dashboard
- **Total Transactions**: Complete transaction count
- **Incoming/Outgoing**: Direction of fund flows
- **Total Volume**: Sum of all transaction amounts
- **Analysis Time**: When the analysis was performed

## 🎨 Customization

### Adding New Cryptocurrencies
1. Extend the `BlockchainTracker` class in `core/blockchain_tracker.py`
2. Add new API integration methods
3. Update the `detect_currency` method
4. Add new visualization options

### Modifying the Web Interface
- Edit `templates/index.html` for frontend changes
- Modify `app.py` for backend API changes
- Update CSS in the HTML file for styling

### CLI Enhancements
- Add new command-line arguments in `blocktracker_cli.py`
- Implement new analysis functions
- Extend the help documentation

## 🔒 Security Considerations

- **API Keys**: Never commit API keys to version control
- **Rate Limiting**: Respect blockchain API rate limits
- **Data Privacy**: Be mindful of blockchain data privacy implications
- **Legal Compliance**: Ensure compliance with local regulations

## 🚨 Troubleshooting

### Common Issues

#### "No transactions found"
- Check if the address is valid
- Verify the cryptocurrency is supported
- Ensure API keys are configured correctly

#### "Network error"
- Check internet connection
- Verify API endpoints are accessible
- Check API rate limits

#### "Import error"
- Ensure all dependencies are installed
- Check Python version compatibility
- Verify file paths and imports

### Debug Mode
Enable debug mode for detailed error information:
```bash
export FLASK_DEBUG=1
python app.py
```

## 📈 Performance Tips

- **Batch Analysis**: Use the CLI for analyzing multiple addresses
- **Caching**: Results are cached to avoid repeated API calls
- **Rate Limiting**: Built-in delays to respect API limits
- **Parallel Processing**: Multiple addresses can be analyzed simultaneously

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Original Author**: Keany Vy KHUN for the foundational BlockTracker project
- **Blockchain APIs**: Etherscan, Blockstream, TronGrid for providing data access
- **Open Source Libraries**: NetworkX, Flask, Bootstrap, and many others

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check this README and inline code comments
- **Community**: Join discussions in the project's GitHub community

## 🔮 Future Roadmap

- [ ] Support for more cryptocurrencies (Cardano, Polkadot, etc.)
- [ ] Machine learning-based end receiver prediction
- [ ] Real-time transaction monitoring
- [ ] Mobile app development
- [ ] Advanced analytics and reporting
- [ ] Integration with blockchain analytics tools

---

**Happy Blockchain Tracking! 🚀** 