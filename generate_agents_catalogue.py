# generate_agents_catalogue.py
"""
Generate a catalogue of 1000 agents for the AI Agent Civilization.
Most will be stubs (no source), a few will be placeholder open-source URLs.
"""
import yaml

def generate_agents():
    agents = []
    specializations = [
        "data_processor", "api_integrator", "db_manager", "code_generator",
        "network_client", "test_runner", "builder", "designer", "reviewer",
        "educator", "monitor", "modifier", "surgeon", "self_developer",
        "architect", "analyst", "researcher", "strategist", "communicator"
    ]
    # We'll create 1000 agents, cycling through specializations and adding indices
    for i in range(1000):
        spec_idx = i % len(specializations)
        name = f"{specializations[spec_idx]}_{i:04d}"
        # For the first 10, we pretend they have open-source repos (placeholder URLs)
        if i < 10:
            source = f"https://github.com/example/{name}.git"
            branch = "main"
        else:
            source = None  # will generate stub
            branch = None
        agents.append({
            "name": name,
            "source": source,
            "branch": branch,
            "specialization": f"domain_specialists/{specializations[spec_idx]}" if source else f"domain_specialists/{specializations[spec_idx]}"
        })
    return {"agents": agents}

if __name__ == "__main__":
    data = generate_agents()
    with open("agents.yaml", "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    print("Generated agents.yaml with 1000 agents")