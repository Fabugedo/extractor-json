# Structured Email Extractor (Learning Project)

This project documents my learning process designing a structured data extractor using LLM-style system prompts and JSON schema validation.

The goal is to transform unstructured support emails into a clean, validated JSON format.

---

## Objective

Given a messy support email, generate a JSON response that:

- Follows a strict contract
- Uses controlled enumerations
- Handles missing data explicitly
- Separates structural validation from business validation
- Includes structured error reporting

---

## Project Structure

structured-email-extractor/
├── contracts/
│ └── contract_v1.schema.json
├── prompts/
│ └── system_prompt_v2.txt
├── tests/
│ ├── email_01_clean.txt
│ ├── email_02_ambiguous.txt
│ └── email_03_missing_order_id.txt
├── outputs/
│ ├── email_01_clean.json
│ ├── email_02_ambiguous.json
│ └── email_03_missing_order_id.json
└── validate_outputs.py


---

## Contract Design

The extractor must always return a JSON object with:

- `customer`
- `request`
- `errors`

Key design decisions:

- `order_id` is mandatory (non-empty string)
- If missing in the email, it is set to `"MISSING"` and an error is added
- `urgency` is restricted to:
  - `"low"`
  - `"medium"`
  - `"high"`
  - `"unknown"`
- Email format is validated using JSON Schema (`format: email`)
- No additional properties are allowed

---

## Validation Strategy

The project uses:

- JSON Schema (Draft 2020-12)
- Python `jsonschema` library
- `FormatChecker` for email validation

Two validation layers exist:

1. Structural validation (schema)
2. Business validation (`errors` array)

Structural errors cause validation failure.
Business errors are reported inside the JSON.

---

## Example: Missing Order ID

```json
{
  "request": {
    "order_id": "MISSING"
  },
  "errors": ["missing_order_id"]
}
