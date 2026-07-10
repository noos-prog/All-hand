"""
CGP Skills Module
================

Primitive skills - the smallest unit of capability.
"""

from .primitive import (
    Skill, SkillCategory, SkillDifficulty,
    SkillRegistry, SkillExtractor
)

__all__ = [
    "Skill",
    "SkillCategory",
    "SkillDifficulty",
    "SkillRegistry",
    "SkillExtractor",
]
