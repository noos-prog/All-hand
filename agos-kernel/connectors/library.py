"""AGOS Enterprise Connectors Library."""
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ConnectorMetadata:
    """Connector metadata."""
    id: str
    name: str
    provider: str
    version: str = "1.0.0"
    description: str = ""


class Connector:
    """An enterprise connector."""
    
    def __init__(self, name: str, provider: str, description: str = ""):
        self.metadata = ConnectorMetadata(
            id=f"conn-{uuid.uuid4().hex[:8]}",
            name=name,
            provider=provider,
            description=description,
        )
        self.capabilities: List[str] = []
        self.auth_types: List[str] = []
        self.rate_limits: Dict[str, int] = {}


# Connectors
CONNECTORS = {
    # Version Control
    "github": Connector("GitHub", "GitHub", "GitHub API connector"),
    "gitlab": Connector("GitLab", "GitLab", "GitLab API connector"),
    "bitbucket": Connector("Bitbucket", "Atlassian", "Bitbucket API connector"),
    "azure_devops": Connector("Azure DevOps", "Microsoft", "Azure DevOps connector"),
    
    # Project Management
    "jira": Connector("Jira", "Atlassian", "Jira connector"),
    "confluence": Connector("Confluence", "Atlassian", "Confluence connector"),
    "linear": Connector("Linear", "Linear", "Linear connector"),
    "notion": Connector("Notion", "Notion", "Notion connector"),
    
    # Communication
    "slack": Connector("Slack", "Slack", "Slack connector"),
    "teams": Connector("Microsoft Teams", "Microsoft", "Teams connector"),
    "discord": Connector("Discord", "Discord", "Discord connector"),
    
    # Storage
    "google_drive": Connector("Google Drive", "Google", "Google Drive connector"),
    "onedrive": Connector("OneDrive", "Microsoft", "OneDrive connector"),
    "dropbox": Connector("Dropbox", "Dropbox", "Dropbox connector"),
    "sharepoint": Connector("SharePoint", "Microsoft", "SharePoint connector"),
    
    # Email
    "gmail": Connector("Gmail", "Google", "Gmail connector"),
    "outlook": Connector("Outlook", "Microsoft", "Outlook connector"),
    
    # Support
    "zendesk": Connector("Zendesk", "Zendesk", "Zendesk connector"),
    "servicenow": Connector("ServiceNow", "ServiceNow", "ServiceNow connector"),
    
    # CRM
    "salesforce": Connector("Salesforce", "Salesforce", "Salesforce connector"),
    "hubspot": Connector("HubSpot", "HubSpot", "HubSpot connector"),
    
    # Payments
    "stripe": Connector("Stripe", "Stripe", "Stripe connector"),
    "paypal": Connector("PayPal", "PayPal", "PayPal connector"),
    
    # Cloud
    "aws": Connector("AWS", "Amazon", "AWS connector"),
    "azure": Connector("Azure", "Microsoft", "Azure connector"),
    "gcp": Connector("Google Cloud", "Google", "GCP connector"),
    "cloudflare": Connector("Cloudflare", "Cloudflare", "Cloudflare connector"),
    
    # Container & IaC
    "kubernetes": Connector("Kubernetes", "CNCF", "Kubernetes connector"),
    "docker": Connector("Docker", "Docker", "Docker connector"),
    "terraform": Connector("Terraform", "HashiCorp", "Terraform connector"),
    
    # Databases
    "postgresql": Connector("PostgreSQL", "PostgreSQL", "PostgreSQL connector"),
    "mysql": Connector("MySQL", "MySQL", "MySQL connector"),
    "mongodb": Connector("MongoDB", "MongoDB", "MongoDB connector"),
    "redis": Connector("Redis", "Redis", "Redis connector"),
    
    # Messaging
    "kafka": Connector("Kafka", "Apache", "Kafka connector"),
    "rabbitmq": Connector("RabbitMQ", "RabbitMQ", "RabbitMQ connector"),
    "nats": Connector("NATS", "NATS.io", "NATS connector"),
    
    # AI
    "openai": Connector("OpenAI", "OpenAI", "OpenAI connector"),
    "anthropic": Connector("Anthropic", "Anthropic", "Anthropic connector"),
    "google_ai": Connector("Google AI", "Google", "Google AI connector"),
    "ollama": Connector("Ollama", "Ollama", "Ollama connector"),
    "openrouter": Connector("OpenRouter", "OpenRouter", "OpenRouter connector"),
    
    # Identity
    "ldap": Connector("LDAP", "OpenLDAP", "LDAP connector"),
    "active_directory": Connector("Active Directory", "Microsoft", "AD connector"),
    "oauth": Connector("OAuth", "OAuth", "OAuth connector"),
    "oidc": Connector("OpenID Connect", "OIDC", "OIDC connector"),
    "saml": Connector("SAML", "SAML", "SAML connector"),
    
    # Integration
    "webhook": Connector("Webhook", "Generic", "Webhook connector"),
    "rest": Connector("REST", "Generic", "REST API connector"),
    "graphql": Connector("GraphQL", "GraphQL", "GraphQL connector"),
}


class ConnectorLibrary:
    """Library of enterprise connectors."""
    
    def __init__(self):
        self.connectors = CONNECTORS
    
    def get(self, name: str) -> Connector:
        return self.connectors.get(name)
    
    def list_all(self) -> List[Connector]:
        return list(self.connectors.values())


_library = ConnectorLibrary()


def get_library() -> ConnectorLibrary:
    return _library