import json
import pathlib

from common import make_session

DATA_DIR = pathlib.Path("data") / "ssen"

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with make_session() as session:
        r = session.get("https://www.ssen.co.uk/Sse_Components/Views/Controls/FormControls/PowerTrackHandler.ashx", verify=False)
        r.raise_for_status()

        data = r.json()
        if data:
            for fault in data["Faults"]:
                fault_ref = fault["Reference"]
                print(f"Fault ref: {fault_ref}")

                with open(DATA_DIR / f"{fault_ref}.json", "w", newline="\n", encoding="utf-8") as f:
                    json.dump(fault, f, ensure_ascii=False, indent=2)
