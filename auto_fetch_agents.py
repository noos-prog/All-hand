# auto_fetch_agents.py
"""
Auto-fetch agents: a background service that periodically checks for new open-source agents
and integrates them into the civilization.

This is a demonstration of how the system could automatically discover and pull agents
from a configured list of sources or registries.
"""

import json
import time
import yaml
import hashlib
import requests
from pathlib import Path

CATALOGUE_FILE = "agents.yaml"
STATE_FILE = ".agent_fetch_state.json"


def load_catalogue():
    if not Path(CATALOGUE_FILE).exists():
        return []
    with open(CATALOGUE_FILE, "r") as f:
        data = yaml.safe_load(f)
    return data.get("agents", [])


def load_state():
    if Path(STATE_FILE).exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"known_hashes": {}, "last_check": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def compute_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()


def check_github_repo(repo_url):
    """Check a GitHub repo for changes by comparing commit hash of main branch."""
    # Extract owner/repo from URL
    # https://github.com/owner/repo.git -> owner/repo
    if repo_url.startswith("https://github.com/"):
        repo_path = repo_url.replace("https://github.com/", "").replace(".git", "")
        api_url = f"https://api.github.com/repos/{repo_path}/commits/main"
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                commit = response.json()
                return commit.get("sha")
        except Exception:
            pass
    return None


def auto_fetch_cycle():
    """Run one cycle of checking and fetching."""
    agents = load_catalogue()
    state = load_state()
    changes = False

    for agent in agents:
        source = agent.get("source")
        if not source:
            continue  # generated agent, no source to check

        commit_hash = check_github_repo(source)
        if commit_hash:
            known = state["known_hashes"].get(source)
            if known != commit_hash:
                print(f"🔄 Change detected for {agent['name']} ({source})")
                state["known_hashes"][source] = commit_hash
                changes = True
                # Here we would trigger the clone/pull
                # For now, just log
                print(f"   -> Would fetch update for {agent['name']}")

    state["last_check"] = int(time.time())
    save_state(state)

    if changes:
        print("✅ Auto-fetch cycle completed with changes")
    else:
        print("✅ Auto-fetch cycle completed (no changes)")


def run_daemon(interval_seconds=3600):
    """Run auto-fetch as a daemon."""
    print(f"🤖 Starting auto-fetch daemon (interval: {interval_seconds}s)")
    try:
        while True:
            auto_fetch_cycle()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n🛑 Daemon stopped")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=3600, help="Daemon interval in seconds")
    args = parser.parse_args()

    if args.once:
        auto_fetch_cycle()
    else:
        run_daemon(args.interval)