"""AGOS Framework Packs Library."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class FrameworkPackMetadata:
    """Framework pack metadata."""
    id: str
    name: str
    category: str
    version: str = "1.0.0"
    config_files: List[str] = field(default_factory=list)
    description: str = ""


class FrameworkPack:
    """A framework pack."""
    
    def __init__(self, name: str, category: str, config_files: List[str], description: str = ""):
        """Initialize framework pack."""
        self.metadata = FrameworkPackMetadata(
            id=f"fwk-{uuid.uuid4().hex[:8]}",
            name=name,
            category=category,
            config_files=config_files,
            description=description,
        )
        self.best_practices: List[str] = []
        self.security_policies: List[str] = []
        self.templates: List[Dict] = []


# Framework Packs
FRAMEWORK_PACKS = {
    # Frontend Frameworks
    "react": FrameworkPack("React", "frontend", ["package.json", "tsconfig.json"], "React UI framework"),
    "nextjs": FrameworkPack("Next.js", "frontend", ["next.config.js", "package.json"], "React SSR framework"),
    "vue": FrameworkPack("Vue", "frontend", ["package.json", "vite.config.js"], "Vue.js framework"),
    "nuxt": FrameworkPack("Nuxt", "frontend", ["nuxt.config.ts"], "Vue SSR framework"),
    "angular": FrameworkPack("Angular", "frontend", ["angular.json", "package.json"], "Angular framework"),
    "svelte": FrameworkPack("Svelte", "frontend", ["svelte.config.js"], "Svelte framework"),
    "solidjs": FrameworkPack("SolidJS", "frontend", ["package.json"], "SolidJS framework"),
    "astro": FrameworkPack("Astro", "frontend", ["astro.config.mjs"], "Astro framework"),
    
    # Backend Frameworks
    "express": FrameworkPack("Express", "backend", ["package.json"], "Express.js framework"),
    "nestjs": FrameworkPack("NestJS", "backend", ["nest-cli.json", "package.json"], "NestJS framework"),
    "fastify": FrameworkPack("Fastify", "backend", ["package.json"], "Fastify framework"),
    "hono": FrameworkPack("Hono", "backend", ["package.json"], "Hono framework"),
    "django": FrameworkPack("Django", "backend", ["manage.py", "requirements.txt"], "Django framework"),
    "flask": FrameworkPack("Flask", "backend", ["requirements.txt", "app.py"], "Flask framework"),
    "fastapi": FrameworkPack("FastAPI", "backend", ["requirements.txt", "main.py"], "FastAPI framework"),
    "springboot": FrameworkPack("Spring Boot", "backend", ["pom.xml", "build.gradle"], "Spring Boot framework"),
    "quarkus": FrameworkPack("Quarkus", "backend", ["pom.xml"], "Quarkus framework"),
    "micronaut": FrameworkPack("Micronaut", "backend", ["build.gradle", "pom.xml"], "Micronaut framework"),
    "aspnetcore": FrameworkPack("ASP.NET Core", "backend", ["*.csproj"], "ASP.NET Core framework"),
    "laravel": FrameworkPack("Laravel", "backend", ["composer.json", "artisan"], "Laravel framework"),
    "symfony": FrameworkPack("Symfony", "backend", ["composer.json"], "Symfony framework"),
    "rails": FrameworkPack("Ruby on Rails", "backend", ["Gemfile", "config/routes.rb"], "Rails framework"),
    "phoenix": FrameworkPack("Phoenix", "backend", ["mix.exs"], "Phoenix framework"),
    "gin": FrameworkPack("Gin", "backend", ["go.mod"], "Gin framework"),
    "fiber": FrameworkPack("Fiber", "backend", ["go.mod"], "Fiber framework"),
    "echo": FrameworkPack("Echo", "backend", ["go.mod"], "Echo framework"),
    "actix": FrameworkPack("Actix", "backend", ["Cargo.toml"], "Actix framework"),
    "axum": FrameworkPack("Axum", "backend", ["Cargo.toml"], "Axum framework"),
    "rocket": FrameworkPack("Rocket", "backend", ["Cargo.toml"], "Rocket framework"),
    
    # Mobile Frameworks
    "flutter": FrameworkPack("Flutter", "mobile", ["pubspec.yaml"], "Flutter framework"),
    "reactnative": FrameworkPack("React Native", "mobile", ["package.json"], "React Native framework"),
    "expo": FrameworkPack("Expo", "mobile", ["app.json", "package.json"], "Expo framework"),
    "electron": FrameworkPack("Electron", "desktop", ["package.json"], "Electron framework"),
    "tauri": FrameworkPack("Tauri", "desktop", ["Cargo.toml", "tauri.conf.json"], "Tauri framework"),
    "unity": FrameworkPack("Unity", "gaming", ["*.unity"], "Unity game engine"),
    "unreal": FrameworkPack("Unreal Engine", "gaming", ["*.uproject"], "Unreal Engine"),
    
    # AI/ML Frameworks
    "tensorflow": FrameworkPack("TensorFlow", "ml", ["requirements.txt"], "TensorFlow framework"),
    "pytorch": FrameworkPack("PyTorch", "ml", ["requirements.txt"], "PyTorch framework"),
    "keras": FrameworkPack("Keras", "ml", ["requirements.txt"], "Keras framework"),
    "langchain": FrameworkPack("LangChain", "ai", ["requirements.txt"], "LangChain framework"),
    "llamaindex": FrameworkPack("LlamaIndex", "ai", ["requirements.txt"], "LlamaIndex framework"),
    "haystack": FrameworkPack("Haystack", "ai", ["requirements.txt"], "Haystack framework"),
    
    # Data Frameworks
    "spark": FrameworkPack("Apache Spark", "data", ["build.sbt"], "Apache Spark framework"),
    "flink": FrameworkPack("Apache Flink", "data", ["pom.xml"], "Apache Flink framework"),
    "airflow": FrameworkPack("Airflow", "data", ["requirements.txt"], "Airflow framework"),
    "dbt": FrameworkPack("dbt", "data", ["dbt_project.yml"], "dbt framework"),
    
    # Backend-as-a-Service
    "supabase": FrameworkPack("Supabase", "baas", ["supabase.json"], "Supabase framework"),
    "firebase": FrameworkPack("Firebase", "baas", ["firebase.json"], "Firebase framework"),
    
    # ORM Frameworks
    "prisma": FrameworkPack("Prisma", "orm", ["schema.prisma"], "Prisma ORM"),
    "drizzle": FrameworkPack("Drizzle", "orm", ["drizzle.config.ts"], "Drizzle ORM"),
    "typeorm": FrameworkPack("TypeORM", "orm", ["ormconfig.json"], "TypeORM framework"),
    "sequelize": FrameworkPack("Sequelize", "orm", ["sequelize.json"], "Sequelize ORM"),
    "mikroorm": FrameworkPack("MikroORM", "orm", ["mikro-orm.config.ts"], "MikroORM"),
    "mongoose": FrameworkPack("Mongoose", "orm", [], "Mongoose ODM"),
    "redis": FrameworkPack("Redis Stack", "cache", ["package.json"], "Redis Stack"),
    "elasticsearch": FrameworkPack("Elasticsearch", "search", [], "Elasticsearch"),
    "neo4j": FrameworkPack("Neo4j", "graph", [], "Neo4j Graph DB"),
    
    # Observability
    "opentelemetry": FrameworkPack("OpenTelemetry", "observability", [], "OpenTelemetry"),
    "kafka": FrameworkPack("Kafka Streams", "streaming", [], "Kafka Streams"),
}


class FrameworkPackLibrary:
    """Library of framework packs."""
    
    def __init__(self):
        self.packs = FRAMEWORK_PACKS
    
    def get(self, name: str) -> FrameworkPack:
        return self.packs.get(name)
    
    def list_all(self) -> List[FrameworkPack]:
        return list(self.packs.values())
    
    def list_by_category(self, category: str) -> List[FrameworkPack]:
        return [p for p in self.packs.values() if p.metadata.category == category]


_library = FrameworkPackLibrary()


def get_library() -> FrameworkPackLibrary:
    return _library