import os

from dsm.roche.util.api import API
# from dsm.roche.util.logger_util import get_logger

# logger = get_logger(__name__)
host = os.getenv("QATEST_URL")
# username = "s***@fortanix.com"
# password = "t***"
username = os.getenv("QATEST_EMAIL")
password = os.getenv("QATEST_PASSWORD")
users = [
    {
        "Email": "sysadmin@fortanix.com",
        "First_Name": "Sysadmin",
        "Last_Name": "Test",
        "Password": "test123#",
        "Role": "ACCOUNTADMINISTRATOR",
    },
    {
        "Email": "qa1@fortanix.com",
        "First_Name": "QA1",
        "Last_Name": "Test",
        "Password": "Fortanix@2021",
        "Role": "ACCOUNTADMINISTRATOR",
    },
    {
        "Email": "qa2@fortanix.com",
        "First_Name": "QA2",
        "Last_Name": "Test",
        "Password": "Fortanix@2021",
        "Role": "ACCOUNTADMINISTRATOR",
    },
    {
        "Email": "qa3@fortanix.com",
        "First_Name": "QA3",
        "Last_Name": "Test",
        "Password": "Fortanix@2021",
        "Role": "ACCOUNTADMINISTRATOR",
    },
    {
        "Email": "qa4@fortanix.com",
        "First_Name": "QA4",
        "Last_Name": "Test",
        "Password": "Fortanix@2021",
        "Role": "ACCOUNTADMINISTRATOR",
    },
    {
        "Email": "qa5@fortanix.com",
        "First_Name": "QA5",
        "Last_Name": "Test",
        "Password": "Fortanix@2021",
        "Role": "ACCOUNTADMINISTRATOR",
    },
    {
        "Email": "qa6@fortanix.com",
        "First_Name": "QA6",
        "Last_Name": "Test",
        "Password": "Fortanix@2021",
        "Role": "ACCOUNTADMINISTRATOR",
    },
]
if host[-1] != "/":
    host = host + "/"
print(f"host = {host}")
api = API(host, username, password)
api.select_account("278fec9c-aa19-4075-a81e-5bca9649a136")
user_emails = api.get_all_users()
emails = [user["user_email"] for user in user_emails]
emails = {e.lower() for e in emails}
users_not_present = set()  # Using a set for O(1) average lookup time
for user in users:
    test_user_email = user["Email"]
    roles = user["Role"].split()
    print(f"email of test user = {test_user_email} of type = {type(test_user_email)} and Roles: {roles}")
    if test_user_email not in emails:
        # Create user who isn't present in DB
        print(f"User not found: {test_user_email} - will be added to the list")
        users_not_present.add(test_user_email)
        print(f"Creating user: {test_user_email} in DB")
        api.create_user(test_user_email, user["Password"], user["First_Name"], user["Last_Name"])
    # Invite all test user as sysadmin
    api.sysadmin_user_invite(test_user_email, roles, user["First_Name"], user["Last_Name"])
for user in users:
    print("Accept sysadmin invite now")
    api = API(host, user["Email"], user["Password"])
    # Accept sysadmin invite
    api.accept_account_invite("278fec9c-aa19-4075-a81e-5bca9649a136")
# Log all users created by script
if users_not_present:
    print(f"Users added: {', '.join(users_not_present)}")