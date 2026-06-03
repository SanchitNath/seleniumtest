# flake8:noqa
import os
import re
from pathlib import Path


def get_markers():
    # When you use "results = marker_list = []", both refer to the same list object in memory.
    results_co = []
    results = []
    marker_list = []
    cwd = os.getcwd()
    print(f"current working directory -> {cwd}")
    # sysadmin_marker_list = [
    #     "SysadminDummyTest",
    #     "SysAdmin_01",
    #     "SysAdmin_02",
    #     "SysAdmin_03",
    #     "SysAdmin_04",
    #     "SysAdmin_05",
    #     "SysAdminAccountVerification",
    #     "SysAdminLogManagement",
    #     "SysAdminSitSubscriptionWithAddOns_01",
    #     "SysAdminSitSubscriptionWithAddOns_02",
    #     "SysAdminSitSubscriptionWithoutAddOns_01",
    #     "SysAdminSitSubscriptionWithoutAddOns_02",
    #     "Signup",
    # ]
    cr_marker_list = [
        "AmazonSesEmail",
        "ForgotPasswordRecaptcha",
        "Onprem_Sysadmin_Restart",
        "Saas_Sysadmin_Restart",
        "Pending_Invite_Users",
        "Saas_Custom_Login",
        "Saas_Custom_Logo",
        "SysadminAuditlogPurge",
        "SysadminLDAPIntegration",
        "SysadminSAMLIntegration",
        "Sysadmin_Email_Set",
        "Sysadmin_Operator",
        "Sysadmin_Policies_Reset",
        "Sysadmin_Policies_Verification",
        "TrustedCA1",
        "SysadminOAUTHIntegration",
        "Cluster_Restart",
        "Cluster_Restart_01",
        "Cluster_Restart_02",
        "Unverified_Users",
    ]
    ignore_list = [
        "DummyTest",
        "CreateOps",
        "MFA_Regression",
        "CreateOps",
        "TrustedCAReset",
        "AzureManagedHSM",
    ]
    combined_filter = set(cr_marker_list + ignore_list)
    pattern_co = r"#\s*@pytest\.mark\.([A-Za-z0-9_]+)"
    pattern = r"(?<!#)\bmark\.(?!usefixtures|skip|parametrize|run|depend|GCPRotate|SysAdmin|Sysadmin|Signup|DSM_BLS|dast_scan|DSM_MFA)([A-Za-z0-9_]+)"
    current_dir = Path(__file__).resolve().parent
    print(f"Current directory as per Path = {current_dir}")
    # Navigate back two levels and into 'tests'
    folder_path = current_dir.parent.parent / "tests"
    print(f"Path = {folder_path}")
    if not os.path.exists(folder_path):
        print(f"Error: Path {folder_path} does not exist.")
        return
    # Logic-1 to get all markers which has "# @pytest.mark.*" as per "pattern_co"
    for filename in os.listdir(folder_path):
        if filename.endswith("_test.py"):
            file_path = os.path.join(folder_path, filename)
            print(f"File path = {file_path}")
            with open(file_path, "r") as file:
                content = file.read()
                matches_co = re.findall(pattern_co, content)
                print(f"Matches_co => {matches_co}")
                if matches_co:
                    results_co.extend(matches_co)
    if results_co:
        print(
            f"Checking commented out -> {results_co[0]}...{results_co[len(results_co)-1]} whose length l0={len(results_co)}"
        )
    # Logic-2 to get all markers which has "mark.*" as per "pattern"
    for filename in os.listdir(folder_path):
        if filename.endswith("_test.py"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r") as file:
                content = file.read()
                matches = re.findall(pattern, content)
                # Don't add any commented out markers
                for match in matches:
                    if match not in results_co:  # exact match check
                        results.append(match)
    print(f"Before sorting -> {results[0]}...{results[len(results)-1]} whose length l1={len(results)}")
    results.sort()
    # print(f"After sorting -> {results} whose length l2={len(results)}")
    sorted_results = sorted(set(results))
    print(
        f"After removing duplicates -> {sorted_results[0]}...{sorted_results[len(sorted_results)-1]} whose length l3={len(sorted_results)}"
    )
    # Logic-3 to prune 'base' markers if a more specific numbered version exists like "1" or "_1"
    marker_numbered_ver = []
    for index, string in enumerate(sorted_results):
        if not any(
            other.startswith(string) and any(char.isdigit() for char in other[len(string) :])
            for other in sorted_results[index + 1 :]
        ):
            marker_numbered_ver.append(string)
    print(f"length l4={len(marker_numbered_ver)}")
    # Logic-4 to remove all markers except for those added in "Sysadmin" and "C.R" pipeline
    for match in marker_numbered_ver:
        if match not in combined_filter:
            marker_list.append(match)
    print(
        f"After filtering -> {marker_list[0]}...{marker_list[len(marker_list)-1]} whose length l5={len(marker_list)}"
    )
    # Write all the markers into a text file with seperator as ', '
    marker_list_path = os.path.join(cwd, "../../data/marker_list.txt")
    with open(marker_list_path, "w") as outfile:
        outfile.write(", ".join(marker_list))

    print(f"Success. Exported {len(marker_list)} markers.")

if __name__ == "__main__":
    get_markers()