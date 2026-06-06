import json
import os
import shutil

import pandas as pd

DATA_DIR = "../csv_temp_report/data"
TEST_CASE_DIR = os.path.join(os.getcwd(), DATA_DIR, "../../test-cases")
OUTPUT_FILE = os.path.join(os.getcwd(), "../helpers/records.csv")
# Dictionary to store only the latest result for each unique test
# Key = historyId, Value = Dictionary of row data
unique_cases = {}
print(f"Reading test cases from: {TEST_CASE_DIR}")

if os.path.exists('reports'):
    print("In")
    shutil.copytree('reports', TEST_CASE_DIR, dirs_exist_ok=True)
for root, _, files in os.walk(TEST_CASE_DIR):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, encoding="utf-8") as f:
                    case = json.load(f)
                # 1. Identify Unique Key
                # 'historyId' is the standard Allure ID for specific test methods + params.
                # Fallback to 'fullName' if historyId is missing.
                unique_key = case.get("historyId") or case.get("fullName") or case.get("name")
                # 2. Extract Timestamp for comparison
                current_start_time = case.get("time", {}).get("start", 0)
                # 3. Construct the Row Data
                row_data = {
                    "Status": case.get("status"),
                    "Start Time": current_start_time,
                    "Suite": case.get("extra", {}).get("parentSuite")
                    or case.get("extra", {}).get("suite")
                    or "Unknown",
                    "Name": case.get("name"),
                }
                # 4. Filter Logic: Keep Latest Only
                if unique_key not in unique_cases:
                    # New test case found
                    unique_cases[unique_key] = row_data
                else:
                    # Duplicate found! Check if this one is newer.
                    existing_start_time = unique_cases[unique_key]["Start Time"]
                    if current_start_time > existing_start_time:
                        unique_cases[unique_key] = row_data
            except Exception as e:
                print(f"⚠️ Error reading {file_path}: {e}")

# Convert the dictionary values (the filtered rows) to a DataFrame
df = pd.DataFrame(list(unique_cases.values()))
# Optional: Sort by Start Time so the CSV is chronological
if not df.empty:
    df = df.sort_values(by="Start Time")
df.to_csv(OUTPUT_FILE, index=False)
print(f"Created helpers/records.csv with {len(df)} unique rows (Duplicates removed)")


