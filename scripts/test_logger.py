from src.utils.logger import log_event

log_event({"stage": "test", "action": "started"})
log_event({"stage": "test", "action": "finished", "count": 42})