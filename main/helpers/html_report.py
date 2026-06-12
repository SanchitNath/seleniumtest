import os
import sys
import csv
import datetime

# ----------------- #
# 1. SETUP & CONFIG #
# ----------------- #

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
# NOTE: Removed the line above since we are assuming all external dependencies are out.

TEST_URL = os.getenv("TEST_URL")
BUILD_NUMBER = os.getenv("BUILD_NUMBER")
if len(sys.argv) >= 3:
    BUILD_NUMBER = sys.argv[1]
    TEST_URL = sys.argv[2]

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "records.csv")

# Hardcoded Environment Details
env_details = {"Cluster": TEST_URL, "Build": BUILD_NUMBER}
# env_details = {"Cluster": "https://autotest.fortanix.com/", "Build": "5.2.2859-3357"}
now = datetime.datetime.now()
report_date = now.strftime("%a, %d %b %Y %H:%M:%S")

# ----------------------------------- #
# 2. READING, PROCESSING, AND COUNTING #
# ----------------------------------- #

# List to hold the processed test records
test_records = []
total_tests = 0
pass_count = 0
fail_count = 0
skip_count = 0
error_count = 0

# NOTE: Allure's standard columns are case-sensitive: 'Status', 'Start Time', 'Suite', 'Name'
COLUMNS = ["#", "Status", "Start Time", "Suite", "Name"]

try:
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        # Read Header to find column indices
        header = next(reader)
        status_idx = header.index("Status")
        start_time_idx = header.index("Start Time")
        suite_idx = header.index("Suite")
        name_idx = header.index("Name")

        # Process the data rows
        for i, row in enumerate(reader):
            total_tests += 1
            row_number = i + 1
            status = row[status_idx]

            # 3. Counting Test Statistics (Replaces Pandas value_counts)
            if status == "passed":
                pass_count += 1
            elif status == "failed":
                fail_count += 1
            elif status == "skipped":
                skip_count += 1
            elif status == "broken":  # Allure often uses 'broken' for errors
                error_count += 1

            # Store the filtered data
            test_records.append(
                {
                    "#": row_number,
                    "Status": status,
                    "Start Time": row[start_time_idx],
                    "Suite": row[suite_idx],
                    "Name": row[name_idx],
                }
            )

except FileNotFoundError:
    print(f"ERROR: File not found at {csv_path}")
    sys.exit(1)
except ValueError as e:
    print(f"ERROR: Missing expected column in CSV: {e}")
    sys.exit(1)

print(f"Successfully processed {total_tests} records.")


# ------------------------------------ #
# 3. MANUAL HTML REPORT GENERATION     #
# (Replaces the custom build_table)    #
# ------------------------------------ #

# A minimal example of an HTML report structure.
# Full styling ('blue_light') would require extensive CSS, not shown here.


def generate_html_report(records, env, date, total, passed, failed, skipped, error):
    # Summary Table HTML
    summary_html = f"""
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Report Date</td><td>{date}</td></tr>
        <tr><td>Cluster</td><td>{env['Cluster']}</td></tr>
        <tr><td>Build</td><td>{env['Build']}</td></tr>
        <tr><td>Total Tests</td><td>{total}</td></tr>
        <tr><td style="color: green;">Passed</td><td>{passed}</td></tr>
        <tr><td style="color: red;">Failed</td><td>{failed}</td></tr>
        <tr><td style="color: gray;">Skipped</td><td>{skipped}</td></tr>
        <tr><td style="color: orange;">Error/Broken</td><td>{error}</td></tr>
    </table>
    """

    # Detail Table Header
    detail_header_html = "<tr><th>#</th><th>Status</th><th>Start Time</th><th>Suite</th><th>Name</th></tr>"

    # Detail Table Rows
    detail_rows_html = ""
    for record in records:
        status_color = "green" if record["Status"] == "passed" else "red" if record["Status"] == "failed" else "gray"
        detail_rows_html += f"""
        <tr>
            <td>{record['#']}</td>
            <td style="color: {status_color};"><b>{record['Status']}</b></td>
            <td>{record['Start Time']}</td>
            <td>{record['Suite']}</td>
            <td>{record['Name']}</td>
        </tr>
        """

    # Full HTML Page Structure (Minimal)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Execution Report</title>
        <style>
            /* Minimal styling for clarity. 'blue_light' theme goes here */
            body {{ font-family: sans-serif; }}
            table {{ border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Test Summary</h2>
        {summary_html}

        <h2>Test Details ({total} Tests)</h2>
        <table>
            {detail_header_html}
            {detail_rows_html}
        </table>
    </body>
    </html>
    """
    return html_content


html_report = generate_html_report(
    test_records, env_details, report_date, total_tests, pass_count, fail_count, skip_count, error_count
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_report)