import json
import pathlib
import urllib.parse
from typing import Iterator

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

DATA_DIR = pathlib.Path("data") / "ukpowernetworks"
RETRIES = 3
TIMEOUT = 5


def get_incident_ids(session: requests.Session) -> Iterator[str]:
    r = session.get("https://www.ukpowernetworks.co.uk/Incidents/GetIncidents", timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()

    for incident in data["Incidents"]:
        try:
            panel_content_url = incident["PanelContentUrl"]
        except KeyError:
            continue

        url = urllib.parse.urlparse(panel_content_url)
        qs = urllib.parse.parse_qs(url.query)
        try:
            incident_id = qs["incidentId"][0]
        except KeyError:
            continue

        yield incident_id


def get_incident_details(session: requests.Session, incident_id: str) -> dict:
    r = session.get(f"https://www.ukpowernetworks.co.uk/Incidents/getincidentdetails?incidentid={incident_id}", timeout=TIMEOUT)
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
            print(f"Incident reference: {incident_id}")
            incident = get_incident_details(session, incident_id)

            # Remove timestamp field as it seems to change regardless
            try:
                del incident["UKPNIncident"]["Timestamp"]
            except KeyError:
                pass

            with open(DATA_DIR / f"{incident_id}.json", "w", newline="\n", encoding="utf-8") as f:
                json.dump(incident, f, ensure_ascii=False, indent=2)


