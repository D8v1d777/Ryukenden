import json
from typing import Any, Dict, List
from urllib.parse import urlparse
from core.base import BaseModule

class CorrelationEngine(BaseModule):
    """
    Engine to correlate disparate forensic artifacts into a unified intelligence graph.
    Identifies relationships between images, domains, IPs, files, and hashes.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.logger.info("CorrelationEngine module initialized.")

    def build_graph(self, data_inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes multiple analysis results to identify links and build a graph.
        
        Args:
            data_inputs (List[Dict[str, Any]]): A list of results from various Ryukenden modules.
            
        Returns:
            Dict[str, Any]: A graph structure containing nodes and edges.
        """
        self.logger.info(f"Correlating {len(data_inputs)} analysis inputs.")
        
        nodes: Dict[str, Dict[str, Any]] = {}
        edges: List[Dict[str, str]] = []

        def add_node(node_id: str, node_type: str, metadata: Dict[str, Any] = None):
            if not node_id:
                return
            if node_id not in nodes:
                nodes[node_id] = {
                    "id": node_id,
                    "type": node_type,
                    "metadata": metadata or {}
                }

        def add_edge(source: str, target: str, edge_type: str):
            if not source or not target:
                return
            edge = {"source": source, "target": target, "type": edge_type}
            if edge not in edges:
                edges.append(edge)

        for item in data_inputs:
            module_type = item.get("type")
            data = item.get("data", {})
            metadata = item.get("metadata", {})

            if module_type == "url_analysis":
                self._correlate_url(data, add_node, add_edge)

            elif module_type == "image_analysis":
                self._correlate_image(data, add_node, add_edge)

            elif module_type == "file_analysis":
                self._correlate_file(data, add_node, add_edge)

        graph = {
            "nodes": list(nodes.values()),
            "edges": edges
        }
        
        return graph

    def _correlate_url(self, data, add_node, add_edge):
        hostname = data.get("parsed_url", {}).get("hostname")
        ip = data.get("ip_address")
        
        if hostname:
            add_node(hostname, "domain")
            if ip:
                add_node(ip, "ip")
                add_edge(hostname, ip, "resolved_to")

    def _correlate_image(self, data, add_node, add_edge):
        # Image results often come from a file
        file_path = data.get("file_path") or data.get("file_info", {}).get("path")
        if file_path:
            image_id = f"img_{os.path.basename(file_path)}"
            add_node(image_id, "image", {"path": file_path})
            add_node(file_path, "file")
            # Link the logical image concept to the physical file
            add_edge(image_id, file_path, "linked_to")

    def _correlate_file(self, data, add_node, add_edge):
        path = data.get("file_path") or data.get("file_info", {}).get("path")
        source_url = data.get("source_url")
        hashes = data.get("hashes") or data.get("file_info", {}).get("hashes", {})

        if path:
            add_node(path, "file")
            
            # Correlate File to its Hashes
            if isinstance(hashes, dict):
                for algo, val in hashes.items():
                    if val and val != "error":
                        add_node(val, "hash", {"algorithm": algo})
                        add_edge(val, path, "derived_from")
            
            # Correlate File to its origin Domain
            if source_url:
                parsed = urlparse(source_url)
                if parsed.hostname:
                    add_node(parsed.hostname, "domain")
                    add_edge(path, parsed.hostname, "hosted_on")

    def execute(self, data: Any = None) -> Any:
        """
        Standard execution entry point.
        """
        if not isinstance(data, list):
            self.logger.error("CorrelationEngine requires a list of analysis results.")
            return {"error": "Invalid input: expected list of dictionaries."}
            
        return self.build_graph(data)