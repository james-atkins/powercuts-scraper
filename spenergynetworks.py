import json
import pathlib
import re

from common import make_session

DATA_DIR = pathlib.Path("data") / "spenergynetworks"

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with make_session() as session:
        # Website is quite slow so have a high timeout threshold
        r = session.get("https://www.spenergynetworks.co.uk/pages/power_cuts_map.aspx", timeout=15)

        m = re.search("arrPowercutsPostcodes: (?P<data>\[.*\]),", r.text)
        data = json.loads(m["data"])

        for incident in data:
            incident_ref = incident["INCIDENT_REF"]
            print(f"Incident ref: {incident_ref}")

            with open(DATA_DIR / f"{incident_ref}.json", "w", newline="\n", encoding="utf-8") as f:
                json.dump(incident, f, ensure_ascii=False, indent=2)
