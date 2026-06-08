import os
import signal
import sys
import time
import multiprocessing
from dsm.roche.util.api import API

host = os.getenv("HOST")
username = os.getenv("UserName")
password = os.getenv("Password")


# host = "https://test.domain.net/"
# username = "testuser@domain.com"
# password = "********"

class SomeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


# --- Worker Initialization ---
def worker_init():
    """Initializes a new API instance for each worker process."""
    global api
    try:
        api = API(host, username, password)
    except Exception as e:
        # If the API initialization fails, the worker must exit.
        print(f"Worker API initialization failed: {e}")
        sys.exit(1)


# --- Signal Handling ---
# Using a non-local/global flag to signal the main loop to stop,
# instead of terminating the entire process group, which prevents cleanup.

# Flag to signal the main loop to stop gracefully
STOP_GRACEFULLY = multiprocessing.Event()


def handle_sigterm(signum, frame):
    """
    Handles SIGINT/SIGTERM by setting a flag, allowing the main loop
    to finish the current pool iteration and exit cleanly, thus calling join().
    """
    print(f"Received signal {signum}. Setting termination flag for graceful shutdown...")
    STOP_GRACEFULLY.set()
    # Let the main loop handle the exit after pool cleanup.


def run_script(account_id):
    """Worker function to process account deletion."""
    try:
        # Check for safety condition
        if "sit.smartkey.io" in host and username == "sanchit.nath@fortanix.com":
            print("Safety check triggered: Do not delete anything.")
            return  # don't raise SystemExit here which might kill the worker pool

        print(f"[{multiprocessing.current_process().name}] Processing account {account_id}")

        # Access the global API instance initialized in worker_init
        if api.get_account_name(account_id) not in ["", "Existing acc", "account does not exist"]:
            local_api = API(host, username, password)
            local_api.select_account(account_id)
            time.sleep(1)
            print("Attempting to delete account before object removal...")
            local_api.delete_account(account_id)

        api.select_account(account_id)
        api.remove_account_objects_delete_account(account_id)
    except Exception as e:
        # Log the error, but the worker process MUST return normally or raise
        # an exception that the pool can handle without immediate termination.
        # "exc_info=True tells the logger to attach the full traceback of the
        # current exception to the log message."
        print(f"Error in run_script for account {account_id}: {e}")


def main():
    # Set the signal handlers
    signal.signal(signal.SIGINT, handle_sigterm)  # Catch Ctrl+C
    signal.signal(signal.SIGTERM, handle_sigterm)  # Catch kill <pid>

    total_run_script = 30
    max_acc_skip = 10
    processes = 25

    for attempt in range(total_run_script):

        if STOP_GRACEFULLY.is_set():
            print("Graceful shutdown requested. Exiting main loop.")
            break

        api_main = API(host, username, password)
        accounts, _ = api_main.get_all_accounts()
        print(f"{len(accounts)} accounts left after {attempt}/{total_run_script}th attempt...")

        try:
            api_main.accept_reject_accounts_invite(False)
        except Exception as e:
            print(f"accept_reject_accounts_invite failed: {e}", exc_info=True)
            raise SomeException("Failed to accept/reject account invites")

        if len(accounts) >= max_acc_skip:
            print(f"Starting pool with {processes} workers to process {len(accounts)} accounts...")
            # Use the 'with' context manager for multiprocessing.Pool
            # This ensures pool.close() and pool.join() are called when exiting the 'with' block.
            with multiprocessing.Pool(processes=processes, initializer=worker_init, maxtasksperchild=1) as pool_obj:
                try:
                    # Use map_async or apply_async with a timeout/check
                    # If pool.map is used, it blocks until all are done or an exception occurs.
                    # Using map_async for better control:
                    async_result = pool_obj.map_async(run_script, accounts)
                    # Loop while waiting to check for the termination flag
                    while not async_result.ready() and not STOP_GRACEFULLY.is_set():
                        time.sleep(0.5)
                    if STOP_GRACEFULLY.is_set():
                        print("Termination flag detected mid-pool run. Terminating workers...")
                        pool_obj.terminate()  # Kill remaining workers
                        break
                        # The 'with' block exit will call join()
                    else:
                        # Wait for results and check for exceptions from workers
                        async_result.get()
                        print("All pool tasks completed. Cleaning up...")
                        # Explicitly close and join to reap processes
                        pool_obj.close()
                        pool_obj.join()
                        print("Pool closed and joined successfully.")
                except Exception as e:
                    # Catches exceptions from workers or map_async itself
                    print(f"Pool operation failed: {e}. Terminating workers...")
                    pool_obj.terminate()  # Ensure all workers are killed
            # The 'with' block has now executed pool_obj.join(), clearing all workers (zombies).
        else:
            print(f"less than {max_acc_skip} accounts left...")
        time.sleep(2)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    """
    [multiprocessing.set_start_method("spawn", force=True)]
    This makes ALL multiprocessing calls in the script (including Pool())
    use the "spawn" method — even if you don't pass a custom context.
    1. So, [with multiprocessing.Pool(...) as pool_obj:] will automatically use
    "spawn" instead of "fork"
    2. No need to rewrite pool calls
    3. Every multiprocessing construct uses spawn
    4. Avoids accidental use of fork anywhere
    5. This line must run before any multiprocessing call
    """
    try:
        main()
    except SystemExit:
        print("Script finished via SystemExit (likely graceful exit).")
    except Exception as e:
        print(f"Unhandled critical error in main execution: {e}")
        sys.exit(1)