from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Evidence:

    type: str

    description: str

    data: Dict = field(
        default_factory=dict
    )


@dataclass
class Finding:

    scanner: str

    vulnerability: str

    severity: str

    confidence: float

    url: str

    parameter: Optional[str] = None

    evidence: List[Evidence] = field(
        default_factory=list
    )

    description: str = ""

    remediation: str = ""