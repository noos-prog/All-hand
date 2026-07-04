"""
Knowledge Graph Versioning
PHASE-02: EXECUTION-000002 - Engineering Knowledge Graph

Version control for the Knowledge Graph.
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from agos_kernel.civilization.knowledge_graph.knowledge_graph import KnowledgeGraph, GraphVersion


@dataclass
class VersionDiff:
    """Difference between two versions."""
    added_nodes: List[Dict] = field(default_factory=list)
    removed_nodes: List[Dict] = field(default_factory=list)
    modified_nodes: List[Dict] = field(default_factory=list)
    added_relationships: List[Dict] = field(default_factory=list)
    removed_relationships: List[Dict] = field(default_factory=list)
    
    @property
    def is_empty(self) -> bool:
        return not any([
            self.added_nodes,
            self.removed_nodes,
            self.modified_nodes,
            self.added_relationships,
            self.removed_relationships,
        ])


class GraphVersioning:
    """
    Graph Versioning System.
    
    Provides:
    - Immutable history
    - Version snapshots
    - Diff between versions
    - Rollback capability
    """
    
    def __init__(self, graph: KnowledgeGraph):
        self.graph = graph
        self._version_storage: List[Tuple[GraphVersion, Dict]] = []
    
    def create_snapshot(self, label: str = "") -> GraphVersion:
        """
        Create a snapshot of the current graph state.
        
        Args:
            label: Optional label for the snapshot
            
        Returns:
            GraphVersion object
        """
        # Create version in graph
        version = self.graph.create_version()
        
        # Store snapshot
        snapshot = {
            'label': label,
            'timestamp': datetime.utcnow().isoformat(),
            'graph_state': self.graph.to_dict(),
            'hash': self._compute_state_hash(),
        }
        
        self._version_storage.append((version, snapshot))
        
        return version
    
    def get_snapshot(self, version: int) -> Optional[Dict]:
        """
        Get a specific version snapshot.
        """
        for v, snapshot in self._version_storage:
            if v.version == version:
                return snapshot
        return None
    
    def get_latest_snapshot(self) -> Optional[Dict]:
        """Get the latest snapshot."""
        if self._version_storage:
            return self._version_storage[-1][1]
        return None
    
    def diff(self, version1: int, version2: int) -> VersionDiff:
        """
        Compute diff between two versions.
        """
        snapshot1 = self.get_snapshot(version1)
        snapshot2 = self.get_snapshot(version2)
        
        if not snapshot1 or not snapshot2:
            return VersionDiff()
        
        state1 = snapshot1['graph_state']
        state2 = snapshot2['graph_state']
        
        diff = VersionDiff()
        
        # Compare nodes
        nodes1 = set(state1.get('nodes', {}).keys())
        nodes2 = set(state2.get('nodes', {}).keys())
        
        added_node_ids = nodes2 - nodes1
        removed_node_ids = nodes1 - nodes2
        common_node_ids = nodes1 & nodes2
        
        for nid in added_node_ids:
            diff.added_nodes.append(state2['nodes'][nid])
        
        for nid in removed_node_ids:
            diff.removed_nodes.append(state1['nodes'][nid])
        
        # Compare common nodes for modifications
        for nid in common_node_ids:
            node1 = state1['nodes'][nid]
            node2 = state2['nodes'][nid]
            
            if self._nodes_differ(node1, node2):
                diff.modified_nodes.append({
                    'node_id': nid,
                    'before': node1,
                    'after': node2,
                })
        
        # Compare relationships
        rels1 = set(state1.get('relationships', {}).keys())
        rels2 = set(state2.get('relationships', {}).keys())
        
        added_rel_ids = rels2 - rels1
        removed_rel_ids = rels1 - rels2
        
        for rid in added_rel_ids:
            diff.added_relationships.append(state2['relationships'][rid])
        
        for rid in removed_rel_ids:
            diff.removed_relationships.append(state1['relationships'][rid])
        
        return diff
    
    def _nodes_differ(self, node1: Dict, node2: Dict) -> bool:
        """Check if two nodes differ."""
        keys_to_check = ['name', 'type', 'path', 'content', 'description']
        
        for key in keys_to_check:
            if node1.get(key) != node2.get(key):
                return True
        
        # Check metadata
        meta1 = node1.get('metadata', {})
        meta2 = node2.get('metadata', {})
        
        if meta1.get('version') != meta2.get('version'):
            return True
        
        return False
    
    def _compute_state_hash(self) -> str:
        """Compute hash of current state."""
        state = self.graph.to_dict()
        content = json.dumps(state, sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def save_versions(self, path: str) -> None:
        """
        Save all versions to disk.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        versions_data = []
        for version, snapshot in self._version_storage:
            versions_data.append({
                'version': version.__dict__,
                'snapshot': snapshot,
            })
        
        with open(path, 'w') as f:
            json.dump(versions_data, f, indent=2, default=str)
        
        print(f"Versions saved to: {path}")
    
    def load_versions(self, path: str) -> None:
        """
        Load versions from disk.
        """
        with open(path, 'r') as f:
            versions_data = json.load(f)
        
        self._version_storage = []
        
        for data in versions_data:
            version = GraphVersion(**data['version'])
            snapshot = data['snapshot']
            self._version_storage.append((version, snapshot))


class GraphDiff:
    """
    Graph Diff Engine.
    
    Computes and displays differences between graphs.
    """
    
    @staticmethod
    def compare(graph1: KnowledgeGraph, graph2: KnowledgeGraph) -> VersionDiff:
        """
        Compare two graphs.
        """
        state1 = graph1.to_dict()
        state2 = graph2.to_dict()
        
        nodes1 = set(state1.get('nodes', {}).keys())
        nodes2 = set(state2.get('nodes', {}).keys())
        
        diff = VersionDiff()
        
        # Added/removed nodes
        for nid in nodes2 - nodes1:
            diff.added_nodes.append(state2['nodes'][nid])
        
        for nid in nodes1 - nodes2:
            diff.removed_nodes.append(state1['nodes'][nid])
        
        # Relationships
        rels1 = set(state1.get('relationships', {}).keys())
        rels2 = set(state2.get('relationships', {}).keys())
        
        for rid in rels2 - rels1:
            diff.added_relationships.append(state2['relationships'][rid])
        
        for rid in rels1 - rels2:
            diff.removed_relationships.append(state1['relationships'][rid])
        
        return diff
    
    @staticmethod
    def format_diff(diff: VersionDiff) -> str:
        """
        Format diff as human-readable string.
        """
        lines = ["Knowledge Graph Diff", "=" * 40]
        
        if diff.added_nodes:
            lines.append(f"\n+ Added Nodes ({len(diff.added_nodes)}):")
            for node in diff.added_nodes[:10]:
                lines.append(f"  + [{node['type']}] {node['name']}")
            if len(diff.added_nodes) > 10:
                lines.append(f"  ... and {len(diff.added_nodes) - 10} more")
        
        if diff.removed_nodes:
            lines.append(f"\n- Removed Nodes ({len(diff.removed_nodes)}):")
            for node in diff.removed_nodes[:10]:
                lines.append(f"  - [{node['type']}] {node['name']}")
            if len(diff.removed_nodes) > 10:
                lines.append(f"  ... and {len(diff.removed_nodes) - 10} more")
        
        if diff.modified_nodes:
            lines.append(f"\n~ Modified Nodes ({len(diff.modified_nodes)}):")
            for node in diff.modified_nodes[:10]:
                lines.append(f"  ~ [{node['after']['type']}] {node['after']['name']}")
        
        if diff.added_relationships:
            lines.append(f"\n+ Added Relationships ({len(diff.added_relationships)}):")
            for rel in diff.added_relationships[:10]:
                lines.append(f"  + [{rel['type']}] {rel['source_name']} -> {rel['target_name']}")
        
        if diff.removed_relationships:
            lines.append(f"\n- Removed Relationships ({len(diff.removed_relationships)}):")
            for rel in diff.removed_relationships[:10]:
                lines.append(f"  - [{rel['type']}] {rel['source_name']} -> {rel['target_name']}")
        
        if diff.is_empty:
            lines.append("\nNo differences found.")
        
        return "\n".join(lines)
