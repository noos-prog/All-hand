"""Alert Management - Alert rules, channels, and notifications."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
import uuid


class NotificationChannel(Enum):
    """Notification channel types."""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    PAGERDUTY = "pagerduty"
    DISCORD = "discord"
    TEAMS = "teams"


@dataclass
class AlertRule:
    """An alert rule definition."""
    rule_id: str
    name: str
    condition: Callable[[Dict[str, Any]], bool]
    severity: str
    is_enabled: bool = True
    cooldown_seconds: int = 300
    last_triggered: Optional[datetime] = None
    
    def should_trigger(self) -> bool:
        if not self.is_enabled:
            return False
        if self.last_triggered:
            elapsed = (datetime.utcnow() - self.last_triggered).total_seconds()
            if elapsed < self.cooldown_seconds:
                return False
        return True


@dataclass
class AlertChannel:
    """An alert notification channel."""
    channel_id: str
    channel_type: NotificationChannel
    name: str
    config: Dict[str, Any] = field(default_factory=dict)
    is_enabled: bool = True


@dataclass
class AlertNotification:
    """An alert notification."""
    notification_id: str
    alert_id: str
    channel: NotificationChannel
    recipient: str
    sent_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "sent"
    error: Optional[str] = None


@dataclass
class AlertEscalation:
    """Alert escalation policy."""
    escalation_id: str
    levels: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_next_level(self, current_level: int) -> Optional[Dict[str, Any]]:
        if current_level < len(self.levels) - 1:
            return self.levels[current_level + 1]
        return None


class AlertManager:
    """Central alert management system."""
    
    def __init__(self):
        self.rules: Dict[str, AlertRule] = {}
        self.channels: Dict[str, AlertChannel] = {}
        self.notifications: Dict[str, AlertNotification] = {}
        self.escalations: Dict[str, AlertEscalation] = {}
    
    def add_rule(self, rule: AlertRule) -> None:
        self.rules[rule.rule_id] = rule
    
    def remove_rule(self, rule_id: str) -> bool:
        if rule_id in self.rules:
            del self.rules[rule_id]
            return True
        return False
    
    def add_channel(self, channel: AlertChannel) -> None:
        self.channels[channel.channel_id] = channel
    
    def remove_channel(self, channel_id: str) -> bool:
        if channel_id in self.channels:
            del self.channels[channel_id]
            return True
        return False
    
    def create_escalation(
        self,
        name: str,
        levels: List[Dict[str, Any]],
    ) -> AlertEscalation:
        escalation = AlertEscalation(
            escalation_id=str(uuid.uuid4()),
            levels=levels,
        )
        self.escalations[name] = escalation
        return escalation
    
    def trigger_rule(self, rule_id: str, context: Dict[str, Any]) -> bool:
        rule = self.rules.get(rule_id)
        if not rule or not rule.should_trigger():
            return False
        
        if rule.condition(context):
            rule.last_triggered = datetime.utcnow()
            return True
        return False
    
    def send_notification(
        self,
        alert_id: str,
        channel_id: str,
        recipient: str,
        message: str,
    ) -> AlertNotification:
        channel = self.channels.get(channel_id)
        
        notification = AlertNotification(
            notification_id=str(uuid.uuid4()),
            alert_id=alert_id,
            channel=channel.channel_type if channel else NotificationChannel.WEBHOOK,
            recipient=recipient,
        )
        
        self.notifications[notification.notification_id] = notification
        return notification
    
    def get_statistics(self) -> Dict[str, Any]:
        return {
            "rules": len(self.rules),
            "channels": len(self.channels),
            "notifications": len(self.notifications),
            "escalations": len(self.escalations),
        }
