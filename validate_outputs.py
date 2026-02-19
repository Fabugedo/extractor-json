import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).parent
SCHEMA_PATH = ROOT / "contracts" / "contract_v1.schema.json"
OUTPUTS_DIR = ROOT / "outputs"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    schema = load_json(SCHEMA_PATH)

    json_files = sorted(OUTPUTS_DIR.glob("*.json"))
    if not json_files:
        print("No hay archivos en /outputs para validar.")
        return

    failures = 0

    for file in json_files:
        data = load_json(file)

        try:
            validator = Draft202012Validator(
                schema,
                format_checker=FormatChecker()
            )
            validator.validate(data)

            print(f"OK  - {file.name}")

        except ValidationError as e:
            failures += 1
            print(f"FAIL- {file.name}")
            print(f"     {e.message}")

    print()
    print(f"Resumen: {len(json_files) - failures} OK / {failures} FAIL")


if __name__ == "__main__":
    main()
