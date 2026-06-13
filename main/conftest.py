import os
import shutil
from main.utils.logger import LogGen
import pytest
from dotenv import load_dotenv

def pytest_configure():
    print("In conftest > configure")
    load_dotenv()

def pytest_addoption(parser):
    parser.addoption("--URL", action="store", help="Missing URL")

def pytest_sessionstart(session):
    print("In conftest > pytest_sessionstart")
    # """
    # Disaster if tests are run in parallel
    folders_to_clean = ['reports', 'screenshot', 'logs']
    for folder in folders_to_clean:
        folder_path = os.path.join(os.getcwd(), folder)
        if os.path.exists(folder_path):
            try:
                # shutil.rmtree deletes the folder and all its contents
                shutil.rmtree(folder_path)
                print(f"Deleted: {folder}")
            except Exception as e:
                print(f"Error deleting {folder}: {e}")
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created fresh: {folder}")
    # """
    # os.environ['URL'] = pytestconfig.getoption("URL")


@pytest.fixture(scope="class", autouse=True)
def setup_logger(request):
    print("Inside setup logger")
    test_file_full_path = str(request.node.fspath)
    print(test_file_full_path)
    print(os.path.basename(test_file_full_path))
    file_name = os.path.splitext(os.path.basename(test_file_full_path))[0]
    print(f"File name is {file_name}")
    # Create the logger using your existing LogGen
    logger = LogGen.loggen()
    # Attach the logger to the class instance (self)
    if request.cls is not None:
        request.cls.logger = logger
    yield logger