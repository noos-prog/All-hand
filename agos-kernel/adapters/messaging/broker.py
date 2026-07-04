"""Messaging Adapters."""
from typing import Any, Dict, List
from ..base import Adapter


# ADAPTER-000037: Kafka Adapter
class KafkaAdapter(Adapter):
    """Apache Kafka messaging adapter."""
    
    def __init__(self):
        super().__init__("Kafka", "kafka", "Apache Kafka Message Streaming")
        self.metadata.auth_types = ["sasl", "ssl"]
        self.metadata.capabilities = ["produce", "consume", "subscribe"]


# ADAPTER-000038: RabbitMQ Adapter
class RabbitMQAdapter(Adapter):
    """RabbitMQ messaging adapter."""
    
    def __init__(self):
        super().__init__("RabbitMQ", "rabbitmq", "RabbitMQ Message Broker")
        self.metadata.auth_types = ["username", "password"]
        self.metadata.capabilities = ["publish", "consume", "queue"]


# ADAPTER-000039: NATS Adapter
class NATSAdapter(Adapter):
    """NATS messaging adapter."""
    
    def __init__(self):
        super().__init__("NATS", "nats", "NATS Message System")
        self.metadata.capabilities = ["publish", "subscribe", "request"]


# ADAPTER-000040: MQTT Adapter
class MQTTAdapter(Adapter):
    """MQTT messaging adapter."""
    
    def __init__(self):
        super().__init__("MQTT", "mqtt", "MQTT IoT Messaging")
        self.metadata.capabilities = ["publish", "subscribe"]


# Registry
MESSAGING_ADAPTERS = {
    "kafka": KafkaAdapter,
    "rabbitmq": RabbitMQAdapter,
    "nats": NATSAdapter,
    "mqtt": MQTTAdapter,
}


def get_adapter(name: str):
    """Get a messaging adapter."""
    adapter_class = MESSAGING_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()