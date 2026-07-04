"""Domain 11-25 Implementations."""
from .base import Domain


# DOMAIN-000011: Cyber Security
class CyberSecurityDomain(Domain):
    """Cyber Security Domain."""
    
    def __init__(self):
        super().__init__("CyberSecurity", "Security engineering")
        
        self.contribute_capability("SecurityAnalysis", "1.0", "Analyze security posture")
        self.contribute_capability("VulnerabilityAnalysis", "1.0", "Analyze vulnerabilities")
        self.contribute_knowledge("patterns", "1.0", {
            "owasp": "OWASP security patterns",
            "zero_trust": "Zero trust architecture",
            "defense_in_depth": "Defense in depth",
        })
        self.contribute_workflow("security_review", "1.0", [
            {"step": "scan", "skill": "AnalyzeSecurity"},
            {"step": "assess", "skill": "AssessRisk"},
            {"step": "report", "skill": "GenerateSecurityReport"},
        ])


# DOMAIN-000012: Data Engineering
class DataEngineeringDomain(Domain):
    """Data Engineering Domain."""
    
    def __init__(self):
        super().__init__("DataEngineering", "Data pipelines and processing")
        
        self.contribute_capability("DataQualityAnalysis", "1.0", "Analyze data quality")
        self.contribute_capability("PipelineAnalysis", "1.0", "Analyze data pipelines")
        self.contribute_knowledge("patterns", "1.0", {
            "etl": "ETL pipeline patterns",
            "streaming": "Stream processing patterns",
            "lakehouse": "Lakehouse architecture",
        })


# DOMAIN-000013: Database Engineering
class DatabaseEngineeringDomain(Domain):
    """Database Engineering Domain."""
    
    def __init__(self):
        super().__init__("DatabaseEngineering", "Database design and optimization")
        
        self.contribute_capability("QueryAnalysis", "1.0", "Analyze query performance")
        self.contribute_capability("SchemaAnalysis", "1.0", "Analyze database schemas")
        self.contribute_knowledge("patterns", "1.0", {
            "normalization": "Database normalization",
            "indexing": "Indexing strategies",
            "sharding": "Database sharding",
        })


# DOMAIN-000014: Artificial Intelligence Engineering
class AIEngineeringDomain(Domain):
    """AI Engineering Domain."""
    
    def __init__(self):
        super().__init__("AIEngineering", "AI system development")
        
        self.contribute_capability("AIAnalysis", "1.0", "Analyze AI systems")
        self.contribute_knowledge("patterns", "1.0", {
            "rag": "Retrieval augmented generation",
            "agent": "AI agent patterns",
            "chain": "Chain of thought patterns",
        })


# DOMAIN-000015: Machine Learning Engineering
class MLEngineeringDomain(Domain):
    """Machine Learning Engineering Domain."""
    
    def __init__(self):
        super().__init__("MLEngineering", "Machine learning systems")
        
        self.contribute_capability("MLAnalysis", "1.0", "Analyze ML systems")
        self.contribute_capability("ModelAnalysis", "1.0", "Analyze ML models")
        self.contribute_knowledge("patterns", "1.0", {
            "training": "ML training patterns",
            "serving": "Model serving patterns",
            "monitoring": "ML monitoring patterns",
        })


# DOMAIN-000016: LLM Engineering
class LLMEngineeringDomain(Domain):
    """LLM Engineering Domain."""
    
    def __init__(self):
        super().__init__("LLMEngineering", "Large language model engineering")
        
        self.contribute_capability("LLMAnalysis", "1.0", "Analyze LLM applications")
        self.contribute_knowledge("patterns", "1.0", {
            "prompting": "Prompt engineering patterns",
            "fine_tuning": "Fine-tuning patterns",
            "evaluation": "LLM evaluation patterns",
        })


# DOMAIN-000017: Computer Vision Engineering
class ComputerVisionDomain(Domain):
    """Computer Vision Engineering Domain."""
    
    def __init__(self):
        super().__init__("ComputerVision", "Computer vision systems")
        
        self.contribute_capability("VisionAnalysis", "1.0", "Analyze vision systems")


# DOMAIN-000018: Embedded Engineering
class EmbeddedEngineeringDomain(Domain):
    """Embedded Engineering Domain."""
    
    def __init__(self):
        super().__init__("EmbeddedEngineering", "Embedded systems development")
        
        self.contribute_capability("EmbeddedAnalysis", "1.0", "Analyze embedded systems")


# DOMAIN-000019: Game Development
class GameDevelopmentDomain(Domain):
    """Game Development Domain."""
    
    def __init__(self):
        super().__init__("GameDevelopment", "Game development")
        
        self.contribute_capability("GameAnalysis", "1.0", "Analyze game architecture")


# DOMAIN-000020: Blockchain Engineering
class BlockchainEngineeringDomain(Domain):
    """Blockchain Engineering Domain."""
    
    def __init__(self):
        super().__init__("BlockchainEngineering", "Blockchain development")
        
        self.contribute_capability("ChainAnalysis", "1.0", "Analyze blockchain systems")


# DOMAIN-000021: Quality Assurance
class QADomain(Domain):
    """Quality Assurance Domain."""
    
    def __init__(self):
        super().__init__("QA", "Quality assurance engineering")
        
        self.contribute_capability("TestAnalysis", "1.0", "Analyze test coverage")
        self.contribute_capability("QualityAnalysis", "1.0", "Analyze quality metrics")
        self.contribute_knowledge("patterns", "1.0", {
            "unit": "Unit testing patterns",
            "integration": "Integration testing patterns",
            "e2e": "End-to-end testing patterns",
        })


# DOMAIN-000022: Enterprise Architecture
class EnterpriseArchitectureDomain(Domain):
    """Enterprise Architecture Domain."""
    
    def __init__(self):
        super().__init__("EnterpriseArchitecture", "Enterprise architecture")
        
        self.contribute_capability("EAAnalysis", "1.0", "Analyze enterprise architecture")
        self.contribute_knowledge("frameworks", "1.0", {
            "togaf": "TOGAF framework",
            "zachman": "Zachman framework",
        })


# DOMAIN-000023: API Engineering
class APIEngineeringDomain(Domain):
    """API Engineering Domain."""
    
    def __init__(self):
        super().__init__("APIEngineering", "API design and development")
        
        self.contribute_capability("APIDesign", "1.0", "Design APIs")
        self.contribute_capability("APIVersioning", "1.0", "Manage API versions")
        self.contribute_knowledge("standards", "1.0", {
            "openapi": "OpenAPI specification",
            "asyncapi": "AsyncAPI specification",
        })


# DOMAIN-000024: Automation Engineering
class AutomationEngineeringDomain(Domain):
    """Automation Engineering Domain."""
    
    def __init__(self):
        super().__init__("AutomationEngineering", "Automation engineering")
        
        self.contribute_capability("WorkflowAnalysis", "1.0", "Analyze workflows")
        self.contribute_knowledge("patterns", "1.0", {
            "orchestration": "Workflow orchestration patterns",
            "choreography": "Service choreography patterns",
        })


# DOMAIN-000025: Knowledge Engineering
class KnowledgeEngineeringDomain(Domain):
    """Knowledge Engineering Domain."""
    
    def __init__(self):
        super().__init__("KnowledgeEngineering", "Knowledge management")
        
        self.contribute_capability("KnowledgeGraphAnalysis", "1.0", "Analyze knowledge graphs")
        self.contribute_capability("OntologyAnalysis", "1.0", "Analyze ontologies")
        self.contribute_knowledge("patterns", "1.0", {
            "ontology": "Ontology design patterns",
            "taxonomy": "Taxonomy patterns",
            "graph": "Knowledge graph patterns",
        })


# Registry
ENGINEERING_DOMAINS = {
    "security": CyberSecurityDomain,
    "data": DataEngineeringDomain,
    "database": DatabaseEngineeringDomain,
    "ai": AIEngineeringDomain,
    "ml": MLEngineeringDomain,
    "llm": LLMEngineeringDomain,
    "cv": ComputerVisionDomain,
    "embedded": EmbeddedEngineeringDomain,
    "games": GameDevelopmentDomain,
    "blockchain": BlockchainEngineeringDomain,
    "qa": QADomain,
    "ea": EnterpriseArchitectureDomain,
    "api": APIEngineeringDomain,
    "automation": AutomationEngineeringDomain,
    "knowledge": KnowledgeEngineeringDomain,
}


def get_domain(name: str) -> Domain:
    """Get an engineering domain."""
    domain_class = ENGINEERING_DOMAINS.get(name)
    if not domain_class:
        raise ValueError(f"Unknown domain: {name}")
    return domain_class()