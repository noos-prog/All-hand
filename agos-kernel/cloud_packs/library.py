"""AGOS Cloud Packs Library."""
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CloudPackMetadata:
    """Cloud pack metadata."""
    id: str
    name: str
    provider: str
    category: str
    version: str = "1.0.0"
    description: str = ""


class CloudPack:
    """A cloud platform pack."""
    
    def __init__(self, name: str, provider: str, category: str, description: str = ""):
        """Initialize cloud pack."""
        self.metadata = CloudPackMetadata(
            id=f"cloud-{uuid.uuid4().hex[:8]}",
            name=name,
            provider=provider,
            category=category,
            description=description,
        )
        self.services: List[str] = []
        self.architecture_templates: List[Dict] = []
        self.deployment_templates: List[Dict] = []
        self.security_policies: List[str] = []


# Cloud Packs
CLOUD_PACKS = {
    # Major Cloud Providers
    "aws": CloudPack("AWS", "Amazon", "iaas", "Amazon Web Services"),
    "azure": CloudPack("Azure", "Microsoft", "iaas", "Microsoft Azure"),
    "gcp": CloudPack("Google Cloud", "Google", "iaas", "Google Cloud Platform"),
    "oracle": CloudPack("Oracle Cloud", "Oracle", "iaas", "Oracle Cloud Infrastructure"),
    "ibm": CloudPack("IBM Cloud", "IBM", "iaas", "IBM Cloud"),
    "alibaba": CloudPack("Alibaba Cloud", "Alibaba", "iaas", "Alibaba Cloud"),
    
    # VPS Providers
    "digitalocean": CloudPack("DigitalOcean", "DigitalOcean", "vps", "DigitalOcean VPS"),
    "linode": CloudPack("Linode", "Akamai", "vps", "Linode VPS"),
    "vultr": CloudPack("Vultr", "Vultr", "vps", "Vultr VPS"),
    
    # Edge & CDN
    "cloudflare": CloudPack("Cloudflare", "Cloudflare", "edge", "Cloudflare CDN & Edge"),
    
    # Platform-as-a-Service
    "vercel": CloudPack("Vercel", "Vercel", "paas", "Vercel Platform"),
    "netlify": CloudPack("Netlify", "Netlify", "paas", "Netlify Platform"),
    "railway": CloudPack("Railway", "Railway", "paas", "Railway Platform"),
    "render": CloudPack("Render", "Render", "paas", "Render Platform"),
    "flyio": CloudPack("Fly.io", "Fly.io", "paas", "Fly.io Platform"),
    "heroku": CloudPack("Heroku", "Salesforce", "paas", "Heroku Platform"),
    
    # Backend-as-a-Service
    "firebase": CloudPack("Firebase", "Google", "baas", "Firebase BaaS"),
    "supabase": CloudPack("Supabase", "Supabase", "baas", "Supabase Cloud"),
    "neon": CloudPack("Neon", "Neon", "serverless", "Neon Serverless Postgres"),
    "planetscale": CloudPack("PlanetScale", "PlanetScale", "serverless", "PlanetScale MySQL"),
    "mongodb_atlas": CloudPack("MongoDB Atlas", "MongoDB", "database", "MongoDB Atlas"),
    "upstash": CloudPack("Upstash", "Upstash", "serverless", "Upstash Serverless"),
    "confluent": CloudPack("Confluent Cloud", "Confluent", "streaming", "Confluent Cloud"),
    
    # Data & Analytics
    "snowflake": CloudPack("Snowflake", "Snowflake", "data", "Snowflake Data Cloud"),
    "databricks": CloudPack("Databricks", "Databricks", "data", "Databricks Platform"),
    
    # Container Orchestration
    "openshift": CloudPack("OpenShift", "Red Hat", "kubernetes", "OpenShift Kubernetes"),
    "rancher": CloudPack("Rancher", "SUSE", "kubernetes", "Rancher Kubernetes"),
    "tanzu": CloudPack("VMware Tanzu", "VMware", "kubernetes", "VMware Tanzu"),
    
    # Private Cloud
    "openstack": CloudPack("OpenStack", "OpenStack", "iaas", "OpenStack Private Cloud"),
    
    # Serverless
    "koyeb": CloudPack("Koyeb", "Koyeb", "serverless", "Koyeb Serverless"),
}


class CloudPackLibrary:
    """Library of cloud packs."""
    
    def __init__(self):
        self.packs = CLOUD_PACKS
    
    def get(self, name: str) -> CloudPack:
        return self.packs.get(name)
    
    def list_all(self) -> List[CloudPack]:
        return list(self.packs.values())
    
    def list_by_category(self, category: str) -> List[CloudPack]:
        return [p for p in self.packs.values() if p.metadata.category == category]
    
    def list_by_provider(self, provider: str) -> List[CloudPack]:
        return [p for p in self.packs.values() if p.metadata.provider == provider]


_library = CloudPackLibrary()


def get_library() -> CloudPackLibrary:
    return _library