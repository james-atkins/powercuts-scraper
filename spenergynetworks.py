import json
import pathlib
import re

from common import make_session
from requests import ConnectionError

DATA_DIR = pathlib.Path("data") / "spenergynetworks"

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with make_session() as session:
        # Website is quite slow so have a high timeout threshold
        try:
            r = session.get("https://www.spenergynetworks.co.uk/pages/power_cuts_map.aspx", timeout=30)
        except ConnectionError:
            pass
        else:
            r.raise_for_status()

            if r.url in ["https://www.spenergynetworks.co.uk/pages/power_cuts_not_available.aspx",
                         "https://www.spenergynetworks.co.uk/pages/500.aspx"]:
                # Not available
                pass
            else:
                m = re.search("arrPowercutsPostcodes: (?P<data>\[.*\]),", r.text)
                data = json.loads(m["data"])
                if data:
                    for incident in data:
                        incident_ref = incident["INCIDENT_REF"]
                        print(f"Incident ref: {incident_ref}")

                        with open(DATA_DIR / f"{incident_ref}.json", "w", newline="\n", encoding="utf-8") as f:
                            json.dump(incident, f, ensure_ascii=False, indent=2)
