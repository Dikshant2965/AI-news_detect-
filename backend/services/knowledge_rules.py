import re


KNOWLEDGE_RULES = [
    {
        "patterns": [
            r"sun.*revolves around.*earth",
            r"earth.*revolves around.*sun.*24 hours",
            r"sun.*orbits.*earth"
        ],
        "verdict": "REFUTES",
        "reason": (
            "The claim contradicts the established fact that Earth orbits "
            "the Sun, while Earth rotates on its axis approximately once every 24 hours."
        ),
        "topic": "astronomy"
    },

    {
        "patterns": [
            r"earth.*third planet.*sun",
            r"earth.*3rd planet.*sun",
            r"third planet.*from.*sun"
        ],
        "verdict": "SUPPORTS",
        "reason": (
            "The claim matches the established fact that Earth is the third "
            "planet from the Sun."
        ),
        "topic": "astronomy"
    }
]


def check_known_claim(claim):
    if not claim:
        return None

    text = claim.lower().strip()

    for rule in KNOWLEDGE_RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, text):
                return {
                    "verdict": rule["verdict"],
                    "probabilities": {
                        "NEI": 0.0,
                        "REFUTES": 1.0 if rule["verdict"] == "REFUTES" else 0.0,
                        "SUPPORTS": 1.0 if rule["verdict"] == "SUPPORTS" else 0.0
                    },
                    "confidence": 1.0,
                    "reason": rule["reason"],
                    "topic": rule["topic"],
                    "source": "Built-in knowledge rule"
                }

    return None