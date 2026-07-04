"""Storage Adapters."""
from typing import Any, Dict, List
from ..base import Adapter


# ADAPTER-000041: S3 Adapter
class S3Adapter(Adapter):
    """AWS S3 storage adapter."""
    
    def __init__(self):
        super().__init__("S3", "s3", "AWS S3 Object Storage")
        self.metadata.auth_types = ["aws_iam", "access_key"]
        self.metadata.capabilities = ["upload", "download", "list", "delete"]


# ADAPTER-000042: Azure Blob Adapter
class AzureBlobAdapter(Adapter):
    """Azure Blob storage adapter."""
    
    def __init__(self):
        super().__init__("AzureBlob", "azure_blob", "Azure Blob Storage")
        self.metadata.auth_types = ["azure_connection_string", "azure_ad"]


# ADAPTER-000043: Google Cloud Storage Adapter
class GCSAdapter(Adapter):
    """Google Cloud Storage adapter."""
    
    def __init__(self):
        super().__init__("GCS", "gcs", "Google Cloud Storage")
        self.metadata.auth_types = ["gcp_service_account"]


# ADAPTER-000044: MinIO Adapter
class MinIOAdapter(Adapter):
    """MinIO storage adapter."""
    
    def __init__(self):
        super().__init__("MinIO", "minio", "MinIO Object Storage")
        self.metadata.auth_types = ["access_key"]


# Registry
STORAGE_ADAPTERS = {
    "s3": S3Adapter,
    "azure_blob": AzureBlobAdapter,
    "gcs": GCSAdapter,
    "minio": MinIOAdapter,
}


def get_adapter(name: str):
    """Get a storage adapter."""
    adapter_class = STORAGE_ADAPTERS.get(name)
    if not adapter_class:
        raise ValueError(f"Unknown adapter: {name}")
    return adapter_class()