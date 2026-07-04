"""Universal Queue Runtime."""
import hashlib
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    Queue, QueueItem, QueueType, QueueStatus
)


class QueueRuntime:
    """Universal Queue Runtime."""
    
    def __init__(self):
        """Initialize queue runtime."""
        self.queues: Dict[str, Queue] = {}
        self.items: Dict[str, QueueItem] = {}
    
    def create_queue(
        self,
        name: str,
        queue_type: QueueType,
        max_size: int = 10000,
        priority_enabled: bool = False,
        dlq_enabled: bool = False,
    ) -> Queue:
        """Create a new queue."""
        queue_id = self._generate_id(name)
        
        queue = Queue(
            id=queue_id,
            name=name,
            queue_type=queue_type,
            max_size=max_size,
            priority_enabled=priority_enabled,
            dlq_enabled=dlq_enabled,
        )
        
        queue.status = QueueStatus.ACTIVE
        
        self.queues[queue_id] = queue
        return queue
    
    def get_queue(self, queue_id: str) -> Optional[Queue]:
        """Get queue by ID."""
        return self.queues.get(queue_id)
    
    def list_queues(
        self,
        queue_type: Optional[QueueType] = None,
        status: Optional[QueueStatus] = None,
    ) -> List[Queue]:
        """List queues with optional filtering."""
        queues = list(self.queues.values())
        
        if queue_type:
            queues = [q for q in queues if q.queue_type == queue_type]
        
        if status:
            queues = [q for q in queues if q.status == status]
        
        return queues
    
    def enqueue(self, queue_id: str, payload: Dict[str, Any], priority: int = 0) -> Optional[QueueItem]:
        """Add an item to the queue."""
        queue = self.queues.get(queue_id)
        if not queue:
            return None
        
        if len(queue.items) >= queue.max_size:
            return None
        
        item = QueueItem(
            id=self._generate_id(f"item-{queue_id}"),
            queue_type=queue.queue_type,
            priority=priority,
            payload=payload,
        )
        
        queue.items.append(item)
        self.items[item.id] = item
        
        return item
    
    def dequeue(self, queue_id: str) -> Optional[QueueItem]:
        """Remove and return an item from the queue."""
        queue = self.queues.get(queue_id)
        if not queue or not queue.items:
            return None
        
        # Sort by priority if enabled
        if queue.priority_enabled:
            queue.items.sort(key=lambda x: x.priority, reverse=True)
        
        item = queue.items.pop(0)
        item.processed_at = datetime.now()
        
        queue.processed_count += 1
        
        return item
    
    def peek(self, queue_id: str, count: int = 10) -> List[QueueItem]:
        """Peek at items without removing them."""
        queue = self.queues.get(queue_id)
        if not queue:
            return []
        
        items = queue.items[:count]
        if queue.priority_enabled:
            items = sorted(items, key=lambda x: x.priority, reverse=True)[:count]
        
        return items
    
    def requeue(self, item_id: str, error: Optional[str] = None) -> bool:
        """Requeue an item for retry."""
        item = self.items.get(item_id)
        if not item:
            return False
        
        item.retries += 1
        if error:
            item.error = error
        
        if item.retries >= item.max_retries:
            # Move to DLQ if enabled
            return False
        
        # Re-add to queue
        for queue in self.queues.values():
            if queue.queue_type == item.queue_type:
                item.status = "pending"
                queue.items.append(item)
                break
        
        return True
    
    def move_to_dlq(self, item_id: str) -> bool:
        """Move an item to the dead letter queue."""
        item = self.items.get(item_id)
        if not item:
            return False
        
        # Find DLQ for this queue type
        for queue in self.queues.values():
            if queue.queue_type == QueueType.DEAD_LETTER:
                item.status = "dead_letter"
                queue.items.append(item)
                return True
        
        return False
    
    def purge_queue(self, queue_id: str) -> int:
        """Remove all items from a queue."""
        queue = self.queues.get(queue_id)
        if not queue:
            return 0
        
        count = len(queue.items)
        queue.items.clear()
        
        return count
    
    def get_queue_stats(self, queue_id: str) -> Dict[str, Any]:
        """Get queue statistics."""
        queue = self.queues.get(queue_id)
        if not queue:
            return {}
        
        return {
            "queue_id": queue.id,
            "queue_name": queue.name,
            "queue_type": queue.queue_type.value,
            "status": queue.status.value,
            "current_size": len(queue.items),
            "max_size": queue.max_size,
            "processed_count": queue.processed_count,
            "failed_count": queue.failed_count,
        }
    
    def monitor_queues(self) -> Dict[str, Dict[str, Any]]:
        """Monitor all queues."""
        stats = {}
        for queue in self.queues.values():
            stats[queue.id] = self.get_queue_stats(queue.id)
        return stats
    
    def _generate_id(self, name: str) -> str:
        """Generate unique ID."""
        unique = f"{name}-{uuid.uuid4().hex[:8]}"
        return hashlib.md5(unique.encode()).hexdigest()[:16]
