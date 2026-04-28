import json
from core.timeline_engine import TimelineEngine

def test_timeline_anomalies():
    config = {"timeline": {"suspicious_window_seconds": 2}}
    engine = TimelineEngine(config)

    # Mock events representing an "Impossible Sequence" 
    # and a "Temporal Paradox"
    events = [
        {
            "type": "process_exec",
            "timestamp": "2026-04-29T10:00:05Z",
            "data": {"process_name": "malware.exe"}
        },
        {
            "type": "url_analysis",
            "timestamp": "2026-04-29T10:00:10Z",
            "data": {"url": "http://evil.com/payload"}
        },
        {
            "type": "file_analysis",
            "timestamp": "2026-04-29T10:00:15Z",
            "data": {
                "file_path": "malware.exe",
                "created": "2026-04-29T10:00:15Z",
                "modified": "2026-04-29T10:00:01Z" # Paradox: modified before created
            }
        }
    ]

    print("[*] Building timeline and detecting anomalies...")
    result = engine.execute(events)
    
    print("\n[CHRONOLOGICAL TIMELINE]")
    for e in result["timeline"]:
        print(f"{e['timestamp']} | {e['type']}")

    print("\n[DETECTED ANOMALIES]")
    print(json.dumps(result["anomalies"], indent=2))

if __name__ == "__main__":
    test_timeline_anomalies()