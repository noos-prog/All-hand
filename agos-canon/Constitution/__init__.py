"""
AGOS Constitution Module
=======================

The Supreme Law of AGOS.
15 articles governing all aspects of the system.

Article I:  The One Brain
Article II: Provider Principle
Article III: Capability Independence
Article IV: Versioning
Article V:  Verification
Article VI: Knowledge Evidence
Article VII: Explainable Decisions
Article VIII: Complete Replaceability
Article IX:  Mobile as Interface
Article X:  Kernel's Role
Article XI: Privacy
Article XII: Specification is Law
Article XIII: The Change Process
Article XIV: Canon Compliance
Article XV:  The Eternal Platform
"""

from .constitution import Constitution, ArticleType, ArticleStatus, ConstitutionalArticle

__all__ = [
    "Constitution",
    "ArticleType",
    "ArticleStatus",
    "ConstitutionalArticle",
]
