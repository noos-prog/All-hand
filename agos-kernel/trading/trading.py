"""AGOS Trading Engine."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class OrderSide(Enum):
    """Order side."""
    BUY = "buy"
    SELL = "sell"


class OrderType(Enum):
    """Order type."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderStatus(Enum):
    """Order status."""
    PENDING = "pending"
    FILLED = "filled"
    PARTIAL = "partial"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """A trading order."""
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TradingEngine:
    """
    Trading Engine.
    
    Manages trading operations.
    
    Usage:
        engine = TradingEngine()
        order = engine.create_order("AAPL", OrderSide.BUY, 100, OrderType.MARKET)
    """
    
    def __init__(self):
        """Initialize trading engine."""
        self._orders: Dict[str, Order] = {}
        self._positions: Dict[str, float] = {}
    
    def create_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        order_type: OrderType,
        price: Optional[float] = None,
    ) -> Order:
        """Create an order."""
        order = Order(
            id=f"order-{uuid.uuid4().hex[:8]}",
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
        self._orders[order.id] = order
        return order
    
    def fill_order(self, order_id: str, quantity: Optional[float] = None) -> bool:
        """Fill an order."""
        order = self._orders.get(order_id)
        if not order or order.status == OrderStatus.FILLED:
            return False
        
        fill_qty = quantity or order.quantity
        order.filled_quantity = fill_qty
        order.status = OrderStatus.FILLED
        
        # Update position
        if order.side == OrderSide.BUY:
            self._positions[order.symbol] = self._positions.get(order.symbol, 0) + fill_qty
        else:
            self._positions[order.symbol] = self._positions.get(order.symbol, 0) - fill_qty
        
        return True
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        order = self._orders.get(order_id)
        if not order:
            return False
        
        order.status = OrderStatus.CANCELLED
        return True
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get an order by ID."""
        return self._orders.get(order_id)
    
    def list_orders(self, status: Optional[OrderStatus] = None) -> List[Order]:
        """List orders."""
        orders = list(self._orders.values())
        if status:
            orders = [o for o in orders if o.status == status]
        return orders
    
    def get_position(self, symbol: str) -> float:
        """Get position for a symbol."""
        return self._positions.get(symbol, 0.0)


# Global instance
_trading_engine: Optional[TradingEngine] = None


def get_trading_engine() -> TradingEngine:
    """Get the global trading engine."""
    global _trading_engine
    if _trading_engine is None:
        _trading_engine = TradingEngine()
    return _trading_engine
