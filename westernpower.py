import json
import pathlib
from typing import List

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

DATA_DIR = pathlib.Path("data") / "westernpower"
RETRIES = 3
TIMEOUT = 5


def get_incident_ids(session: requests.Session) -> List[str]:
    r = session.get("https://powercuts.westernpower.co.uk/__powercuts/getIncidentsAndAlertSummary", timeout=TIMEOUT)

    data = r.json()
    incidents = json.loads(data["incidents"])

    return [incident["id"] for incident in incidents["incidents"]]


def get_incident_details(incident_id: str):
    r = requests.get(f"https://powercuts.westernpower.co.uk/__powercuts/getIncidentById?incidentId={incident_id}", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    retry_strategy = Retry(
        total=RETRIES,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    with requests.Session() as session:
        session.mount("https://", adapter)

        for incident_id in get_incident_ids(session):
            print(f"Getting incident {incident_id}")
            incident = get_incident_details(incident_id)

            with open(DATA_DIR / f"{incident_id}.json", "w", newline="\n", encoding="utf-8") as f:
                json.dump(incident, f, ensure_ascii=False, indent=2)