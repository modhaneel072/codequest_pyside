from dataclasses import dataclass

@dataclass
class SessionState:
    module_index: int = 0
    stage: str = "lesson"  # lesson | quiz | debug | terminal