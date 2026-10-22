from dotenv import load_dotenv
load_dotenv()

from backend.services.evidence import EvidenceProvider

evidence = EvidenceProvider()

queries = [
    "Barack Obama was born in Kenya",
    "RIL Jio IPO Mukesh Ambani fact check",
    "Mukesh Ambani Jio IPO",
]

for query in queries:
    results = evidence.search(query)
    print("\nQUERY:", query)
    print("RESULT COUNT:", len(results))

    for item in results[:2]:
        print("PUBLISHER:", item.get("publisher"))
        print("RATING:", item.get("rating"))
        print("CLAIM:", item.get("claim"))
