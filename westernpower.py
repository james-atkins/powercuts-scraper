import json
import pathlib
from typing import List

import requests

from common import make_session

DATA_DIR = pathlib.Path("data") / "westernpower"


def get_incident_ids(session: requests.Session) -> List[str]:
    r = session.get("https://powercuts.westernpower.co.uk/__powercuts/getIncidentsAndAlertSummary")

    data = r.json()
    incidents = json.loads(data["incidents"])

    return [incident["id"] for incident in incidents["incidents"]]


def get_incident_details(session: requests.Session, incident_id: str):
    r = session.get(f"https://powercuts.westernpower.co.uk/__powercuts/getIncidentById?incidentId={incident_id}")
    r.raise_for_status()
    incident = r.json()
    del incident["lastUpdated"]
    return incident


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with make_session() as session:
        for incident_id in get_incident_ids(session):
            print(f"Incident Id: {incident_id}")
            incident = get_incident_details(session, incident_id)

            with open(DATA_DIR / f"{incident_id}.json", "w", newline="\n", encoding="utf-8") as f:
                json.dump(incident, f, ensure_ascii=False, indent=2)