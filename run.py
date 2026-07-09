#!/usr/bin/env python3
"""
AI Agent Civilization System - Main Entry Point
FIXED: Complete working system with real agent management.
"""

import asyncio
import logging
import signal
import sys
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('main')


class AgentCivilization:
    """Main system controller. FIXED: Proper lifecycle management."""
    
    def __init__(self):
        self.hub = None
        self.orchestrator = None
        self.dispatcher = None
        self.resource_manager = None
        self.workers: List = []
        self.is_running = False
        self._tasks: List[asyncio.Task] = []
        
    async def initialize(self):
        """Initialize the system with all components."""
        logger.info("=" * 60)
        logger.info("AI Agent Civilization System - Initializing...")
        logger.info("=" * 60)
        
        # Import here to avoid circular imports
        from agent_civilization.core.agents.communication_hub import CommunicationHub
        from agent_civilization.agents.infrastructure.orchestrator_agent import SystemOrchestratorAgent
        from agent_civilization.agents.infrastructure.task_dispatcher import TaskDispatcherAgent
        from agent_civilization.agents.infrastructure.resource_manager import ResourceManagerAgent
        from agent_civilization.agents.executors.data_worker import DataWorkerAgent
        
        # Create communication hub
        self.hub = CommunicationHub()
        logger.info("✓ Communication Hub created")
        
        # Create infrastructure agents
        self.orchestrator = SystemOrchestratorAgent("orchestrator", self.hub)
        self.dispatcher = TaskDispatcherAgent("dispatcher", self.hub)
        self.resource_manager = ResourceManagerAgent("resource_manager", self.hub)
        
        # Register infrastructure with hub
        await self.hub.register_agent(self.orchestrator, "orchestrator")
        await self.hub.register_agent(self.dispatcher, "dispatcher")
        await self.hub.register_agent(self.resource_manager, "resource_manager")
        
        # Start infrastructure agents
        self.orchestrator.start()
        self.dispatcher.start()
        self.resource_manager.start()
        
        logger.info("✓ Infrastructure agents started")
        
        # Create worker agents
        num_workers = 10
        for i in range(num_workers):
            worker = DataWorkerAgent(f"worker_{i:03d}", self.hub, worker_id=i)
            await self.hub.register_agent(worker, worker.name)
            worker.start()
            self.workers.append(worker)
            
        logger.info(f"✓ Created {num_workers} worker agents")
        
        # Register workers with dispatcher
        for worker in self.workers:
            msg = await worker.send_to("dispatcher", {
                "action": "register",
                "capabilities": worker.capabilities
            })
            
        logger.info("✓ Workers registered with dispatcher")
        logger.info("=" * 60)
        logger.info("System initialization complete!")
        logger.info("=" * 60)
        
    async def run(self):
        """Main run loop."""
        self.is_running = True
        tick = 0
        
        while self.is_running:
            await asyncio.sleep(5)  # Status update every 5 seconds
            tick += 1
            
            # Print status
            logger.info(f"--- System Status (tick {tick}) ---")
            logger.info(f"  Registered agents: {len(self.hub.get_registered_agents())}")
            logger.info(f"  Hub stats: {self.hub.get_stats()}")
            logger.info(f"  System status: {self.orchestrator.get_system_status()}")
            logger.info(f"  Resource status: {self.resource_manager.get_status()}")
            
            # Distribute some test work
            if tick % 3 == 0:
                for i in range(3):
                    task_id = f"test_task_{tick}_{i}"
                    await self.dispatcher.add_work({
                        "command": "dispatch_task",
                        "task_type": "data_processing",
                        "task_id": task_id,
                        "data": {"input": f"test_data_{i}", "tick": tick}
                    })
                    
    async def shutdown(self):
        """Graceful shutdown."""
        logger.info("Shutting down system...")
        self.is_running = False
        
        # Stop all agents
        for worker in self.workers:
            worker.shutdown()
            
        self.orchestrator.shutdown()
        self.dispatcher.shutdown()
        self.resource_manager.shutdown()
        
        # Wait for tasks to complete
        await asyncio.sleep(1)
        
        logger.info("System shutdown complete")


async def main():
    """Main entry point."""
    system = AgentCivilization()
    
    # Handle signals
    loop = asyncio.get_running_loop()
    
    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(system.shutdown())
        
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await system.initialize()
        await system.run()
    except asyncio.CancelledError:
        logger.info("Main task cancelled")
    except Exception as e:
        logger.error(f"System error: {e}")
        raise
    finally:
        await system.shutdown()


if __name__ == "__main__":
    print("🚀 Starting AI Agent Civilization System...")
    print("   Press Ctrl+C to shutdown\n")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
