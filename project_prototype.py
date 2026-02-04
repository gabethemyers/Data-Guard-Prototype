import ast
from collections import defaultdict
from typing import Any
import pprint

import pandas as pd


def read_vocab()->dict[str,set[str]]:
   df = pd.read_csv('Controlled_Vocab.csv')

   vocab = defaultdict(set)

   for row in df.itertuples():
      vocab[row.vocab_set].add(row.value)

   return vocab

def get_required_fields()->list[str]:
    data_dict_df = pd.read_csv('Data_Dictionary.csv')

    return data_dict_df[data_dict_df['required'].str.lower() == 'yes']['column_name'].tolist()

def validate_dish(dish: dict[str, Any], vocab: dict[str, set], required_fields:list[str]) -> list[str]:
    """
    Performs a multi-pass validation on a single dish record.

    Args:
        dish: A dictionary representing a record from Dish_Attributes_Preview.
        vocab: The lookup dictionary generated from Controlled_Vocab.csv.
        required_fields: A list of fields that must be present.

    Returns:
        List of error strings. If empty, the record is considered 'Safe'.
    """
    errors = []

    # 1. MANDATORY FIELD CHECK
    # As there's no specific invariant for this in Business_Invariants.csv,
    # we'll use a conventional error code for reporting.
    missing_fields = [field for field in required_fields if field not in dish or dish.get(field) is None]
    if missing_fields:
        errors.extend([f"[DDICT-001] E_REQUIRED_FIELD: The required field '{f}' is missing." for f in missing_fields])

    # 2. CONTROLLED VOCABULARY ENFORCEMENT
    for field, vocab_set in vocab.items():
        value = dish.get(field)
        if pd.isna(value) or value is None:
            continue

        if field in dish:
            # Handle string-encoded arrays
            if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    errors.append(f"[INV-002] E_CV_ARRAY: {field} contains a malformed array string: '{value}'.")
                    continue  # Skip further checks for this malformed field

            # Array validation (INV-002)
            if isinstance(value, list):
                for item in value:
                    if item not in vocab_set:
                        errors.append(f"[INV-002] E_CV_ARRAY: {field} contains invalid value '{item}' for set '{field}'.")
            # Scalar validation (INV-001) with case-insensitivity
            else:
                is_invalid_scalar = False
                if isinstance(value, str):
                    if value.lower() not in vocab_set:
                        is_invalid_scalar = True
                elif value not in vocab_set:
                    is_invalid_scalar = True
                
                if is_invalid_scalar:
                    errors.append(f"[INV-001] E_CV_SCALAR: {field}='{value}' is not a valid active controlled vocab value for set '{field}'.")

    # TODO: 3. TASTE LAYER RANGE VALIDATION
    # Based on DB_Constraints: 'All taste/confidence floats constrained to [0,1]'.
    # Loop through keys starting with 'taste_' and verify they are within [0, 1].
    

    # TODO: 4. PROTEIN ETL TRANSFORMATION (The 'Hard' Rule)
    # Implement rule: protein_types = unique(non_null([primary, secondary])).
    # If resulting list is empty, flag 'requires_manual_review' = True.

    # TODO: 5. CRITICAL SAFETY INVARIANT (Allergen Guard)
    # Logic: If dietary_vegan_flag is True, protein_type_primary must not be
    # a non-vegan code (e.g., beef, chicken, shellfish).

    return errors

dish_df = pd.read_csv('Dish_Attributes_Preview.csv', skiprows=1)

one_dish_dict = dish_df.iloc[0].to_dict()

required_fields = get_required_fields()

errors = validate_dish(one_dish_dict, read_vocab(), required_fields)

print("--- Dish Being Validated ---")
pprint.pprint(one_dish_dict)
print("\n--- Vocabulary Loaded ---")
pprint.pprint(dict(read_vocab()))
print("\n--- Required Fields ---")
pprint.pprint(required_fields)
print("\n--- Validation Errors ---")
pprint.pprint(errors)
