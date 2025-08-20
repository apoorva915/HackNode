import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
import traceback
import json
from typing import Any, Dict, Optional

class BlockTrackerLogger:
    """Comprehensive logging system for BlockTracker"""
    
    def __init__(self, name: str = "BlockTracker", log_level: str = "INFO"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup logging handlers for console, file, and error tracking"""
        
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)-20s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for all logs
        file_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "blocktracker.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)-20s | %(lineno)-4d | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler for errors only
        error_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "errors.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)-20s | %(lineno)-4d | %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
        
        # API calls handler
        api_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "api_calls.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        api_handler.setLevel(logging.INFO)
        api_formatter = logging.Formatter(
            '%(asctime)s | API_CALL | %(message)s'
        )
        api_handler.setFormatter(api_formatter)
        self.logger.addHandler(api_handler)
        
        # User actions handler
        user_handler = logging.handlers.RotatingFileHandler(
            logs_dir / "user_actions.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        user_handler.setLevel(logging.INFO)
        user_formatter = logging.Formatter(
            '%(asctime)s | USER_ACTION | %(message)s'
        )
        user_handler.setFormatter(user_formatter)
        self.logger.addHandler(user_handler)
    
    def log_api_call(self, method: str, url: str, status_code: int, response_time: float, 
                     request_data: Optional[Dict] = None, response_data: Optional[Dict] = None,
                     error: Optional[str] = None):
        """Log API call details"""
        extra = {
            'method': method,
            'url': url,
            'status_code': status_code,
            'response_time': f"{response_time:.3f}s"
        }
        
        message = f"API Call: {method} {url}"
        if request_data:
            message += f" | Request: {json.dumps(request_data, default=str)[:200]}"
        if response_data:
            message += f" | Response: {json.dumps(response_data, default=str)[:200]}"
        if error:
            message += f" | Error: {error}"
        
        self.logger.info(message, extra=extra)
    
    def log_user_action(self, action: str, address: str, currency: str, result: str, 
                        details: Optional[Dict] = None):
        """Log user actions for analytics"""
        extra = {
            'action': action,
            'address': address,
            'currency': currency,
            'result': result,
            'details': json.dumps(details, default=str) if details else "None"
        }
        
        message = f"User Action: {action} | Address: {address} | Currency: {currency} | Result: {result}"
        if details:
            message += f" | Details: {json.dumps(details, default=str)}"
        
        self.logger.info(message, extra=extra)
    
    def log_error(self, error: Exception, context: Optional[Dict] = None, 
                  user_address: Optional[str] = None):
        """Log errors with full context"""
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'user_address': user_address
        }
        
        message = f"ERROR: {type(error).__name__}: {str(error)}"
        if context:
            message += f" | Context: {json.dumps(context, default=str)}"
        if user_address:
            message += f" | User Address: {user_address}"
        
        self.logger.error(message, exc_info=True, extra=error_info)
    
    def log_performance(self, operation: str, duration: float, details: Optional[Dict] = None):
        """Log performance metrics"""
        message = f"Performance: {operation} took {duration:.3f}s"
        if details:
            message += f" | Details: {json.dumps(details, default=str)}"
        
        self.logger.info(message)
    
    def log_system_event(self, event: str, details: Optional[Dict] = None):
        """Log system events"""
        message = f"System Event: {event}"
        if details:
            message += f" | Details: {json.dumps(details, default=str)}"
        
        self.logger.info(message)
    
    def log_security_event(self, event: str, details: Optional[Dict] = None, 
                          severity: str = "INFO"):
        """Log security-related events"""
        message = f"Security Event: {event}"
        if details:
            message += f" | Details: {json.dumps(details, default=str)}"
        
        if severity.upper() == "WARNING":
            self.logger.warning(message)
        elif severity.upper() == "ERROR":
            self.logger.error(message)
        else:
            self.logger.info(message)
    
    def log_transaction_analysis(self, address: str, currency: str, 
                                transaction_count: int, end_receivers: int,
                                analysis_time: float, success: bool):
        """Log transaction analysis results"""
        message = f"Transaction Analysis: {address} | {currency} | "
        message += f"Transactions: {transaction_count} | End Receivers: {end_receivers} | "
        message += f"Time: {analysis_time:.3f}s | Success: {success}"
        
        self.logger.info(message)
    
    def log_memory_usage(self):
        """Log memory usage for monitoring"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            self.logger.info(f"Memory Usage: {memory_mb:.2f} MB")
        except ImportError:
            self.logger.debug("psutil not available for memory monitoring")
    
    def log_startup(self, config: Dict[str, Any]):
        """Log system startup information"""
        startup_info = {
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'platform': sys.platform,
            'config': config
        }
        
        message = f"System Startup: BlockTracker Enhanced v2.0 | Config: {json.dumps(config, default=str)}"
        self.logger.info(message)
    
    def log_shutdown(self):
        """Log system shutdown"""
        self.logger.info("System Shutdown: BlockTracker Enhanced v2.0")
    
    def get_logger(self, name: str = None):
        """Get a logger instance"""
        if name:
            return logging.getLogger(f"{self.name}.{name}")
        return self.logger

# Global logger instance
logger = BlockTrackerLogger()

def get_logger(name: str = None):
    """Get a logger instance"""
    if name:
        return BlockTrackerLogger(name)
    return logger 