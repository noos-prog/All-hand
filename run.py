#!/usr/bin/env python3
"""
Entry point for the AI Agent Civilization system.
Loads configuration, starts the communication hub, and initializes the system.
"""

import asyncio
import logging
import yaml
import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from agent_civilization.core.agents import BaseAgent, Message, CommunicationHub

def load_config():
    """Load configuration from config.yaml"""
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    else:
        # Default configuration
        return {
            "network": {
                "protocol": "tcp",
                "port": 8080
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "resources": {
                "max_cpu_per_agent": 1,
                "max_memory_mb_per_agent": 512
            }
        }

def setup_logging(config):
    """Setup logging based on configuration"""
    log_level = getattr(logging, config.get("logging", {}).get("level", "INFO").upper())
    log_format = config.get("logging", {}).get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.basicConfig(level=log_level, format=log_format)
    logger = logging.getLogger(__name__)
    logger.info("Logging configured")

async def main():
    """Main entry point"""
    print("🚀 Starting AI Agent Civilization System...")
    
    # Load configuration
    config = load_config()
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger("main")
    
    # Initialize communication hub
    communication_hub = CommunicationHub()
    
    logger.info("Communication hub initialized")
    logger.info("System ready for agent registration")
    
    # Start the hub's message processing
    hub_task = asyncio.create_task(communication_hub.process_messages())
    
    # Keep the system running
    try:
        while True:
            await asyncio.sleep(1)
            # Optional: print status
            agent_count = len(communication_hub.agents)
            if agent_count > 0:
                logger.info(f"System status: {agent_count} agents registered")
    except KeyboardInterrupt:
        logger.info("Shutting down system...")
        hub_task.cancel()
        try:
            await hub_task
        except asyncio.CancelledError:
            pass
        logger.info("System shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)