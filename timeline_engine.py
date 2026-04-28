from datetime import datetime
from typing import Any, Dict, List, Optional
from core.base import BaseModule

class TimelineEngine(BaseModule):
    """
    Engine to reconstruct a chronological sequence of forensic events.
    Normalizes time data and identifies suspicious patterns in the timeline.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.logger.info("TimelineEngine initialized.")
        
        # Logical order of attack phases for anomaly detection
        self.ttp_order = {
            "url_analysis": 1,   # Initial Access
            "file_analysis": 2,  # Delivery/Staging
            "process_exec": 3    # Execution
        }
        self.suspicious_threshold = self.config.get("timeline.suspicious_window_seconds", 5)

    def _normalize_timestamp(self, ts: Any) -> Optional[datetime]:
        """Converts various timestamp formats into a standard UTC datetime object."""
        if isinstance(ts, datetime):
            return ts
        
        if not isinstance(ts, str):
            return None

        try:
            # Handle ISO format strings (including 'Z' for UTC)
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            # Custom parsing for common forensic formats could be added here
            self.logger.debug(f"Failed to parse timestamp: {ts}")
            return None

    def build_timeline(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merges, normalizes, and sorts events into a chronological list.
        
        Args:
            events: A list of raw event dictionaries from analyzers.
            
        Returns:
            A sorted list of enriched event dictionaries.
        """
        self.logger.info(f"Processing {len(events)} events for timeline reconstruction.")
        
        processed_events = []
        for event in events:
            raw_ts = event.get("timestamp")
            normalized_ts = self._normalize_timestamp(raw_ts)
            
            if not normalized_ts:
                self.logger.warning(f"Skipping event with invalid timestamp: {event.get('event_type')}")
                continue
                
            enriched_event = event.copy()
            enriched_event["normalized_ts"] = normalized_ts
            processed_events.append(enriched_event)

        # Sort chronologically (Stable sort preserves order of same-time events)
        processed_events.sort(key=lambda x: x["normalized_ts"])

        # Detect suspicious sequences
        return self._detect_suspicious_sequences(processed_events)

    def _detect_suspicious_sequences(self, sorted_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifies rapid or anomalous sequences of events."""
        for i in range(1, len(sorted_events)):
            prev_event = sorted_events[i-1]
            curr_event = sorted_events[i]
            
            delta = (curr_event["normalized_ts"] - prev_event["normalized_ts"]).total_seconds()
            
            # Check for rapid execution (e.g., URL access followed immediately by file creation)
            if delta <= self.suspicious_threshold:
                sequence_flag = {
                    "flag": "suspicious_rapid_sequence",
                    "delta_seconds": delta,
                    "description": f"Rapid transition between {prev_event.get('type')} and {curr_event.get('type')}"
                }
                
                if "analysis_flags" not in curr_event:
                    curr_event["analysis_flags"] = []
                curr_event["analysis_flags"].append(sequence_flag)
                
        return sorted_events

    def execute(self, data: Any = None) -> Any:
        """
        Main execution entry point.
        
        Args:
            data: A list of event dictionaries.
        """
        if not isinstance(data, list):
            self.logger.error("TimelineEngine expects a list of events.")
            return []
            
        result = self.build_timeline(data)
        
        # Convert datetime back to ISO string for the final output report
        for event in result["timeline"]:
            event["timestamp"] = event["normalized_ts"].isoformat()
            del event["normalized_ts"]
            
        return result