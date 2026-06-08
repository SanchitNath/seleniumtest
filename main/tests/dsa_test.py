import csv
import glob
import os
from collections import defaultdict, Counter
from itertools import permutations
import pandas as pd
import requests


class TestDSA:
    def length_of_longest_substring(self, s: str) -> int:
        l, max_len, index = 0, 0, 0
        seen = set()
        for r in range(len(s)):
            while s[r] in seen:
                seen.remove(s[l])
                l+=1
            seen.add(s[r])
            if (r - l + 1) > max_len:
                max_len = r - l + 1
                index = l
        longest_sub = s[index : index + max_len]
        print(longest_sub)
        print(max_len)
        return max_len

    def merge_sorted_arrays(self, arr1, arr2):
        i = 0
        j = 0
        merged = []
        while i < len(arr1) and j < len(arr2):
            if arr1[i] <= arr2[j]:
                merged.append(arr1[i])
                i += 1
            else:
                merged.append(arr2[j])
                j += 1
        while i < len(arr1):
            merged.append(arr1[i])
            i += 1
        while j < len(arr2):
            merged.append(arr2[j])
            j += 1
        print(f"Array with duplicates = {merged}")
        merged = list(set(merged))
        return merged

    def count_error_logs_decreasing_order_count_alp_name(self):
        counts = defaultdict(int)
        path = os.path.join(os.getcwd(), "../data/*.txt")
        for log_file in glob.glob(path):
            with open(log_file, 'r') as f:
                for lines in f:
                    # print(f"Lines = {lines}")
                    parts = lines.strip().split('|')
                    if len(parts) >= 3 and parts[1] == 'ERROR':
                        filename = parts[2]
                        counts[filename] += 1
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        print(f"Sorted counts = {sorted_counts}")
        for filename, count in sorted_counts:
            print(f"filename = {filename}, count = {count}")

    def find_non_repeated_nos(self, arr: list):
        # [1,2,3,4,5,5,3,3,2]
        # O(N)
        counts = Counter(arr)
        # {'1':1, '2':2, '3':3, '4': 1, '5':2}
        non_repeated = []
        # O(N)
        for no in arr:
            # O(1)
            if counts[no] == 1:
                non_repeated.append(no)
        return non_repeated

    def find_non_repeated_numbers(self, arr: list):
        non_repeated = []
        seen = set()
        # O(N)
        for no in arr:
            # O(1)
            if no not in seen:
                # O(N)
                if arr.count(no) == 1:
                    non_repeated.append(no)
                # O(1)
                seen.add(no)
        return non_repeated

    @staticmethod
    def permute(str: str, step=0):
        if step == len(str):
            print(''.join(str))
            return
        for i in range(step, len(str)):
            # Swap in-place
            str[step], str[i] = str[i], str[step]
            # Recursive call
            TestDSA.permute(str, step+1)
            # Undo swap
            str[step], str[i] = str[i], str[step]

    def run_permutations(self):
        print("---permute--- with T.C=O(N)")
        s = list('ABC')
        TestDSA.permute(s)

    def print_permutations(self, s: str):
        for perm in permutations(s):
            print(''.join(perm))

    # Output -> Condition -> Loop
    print_perms = lambda s: [print(''.join(p)) for p in permutations(s)]
    print("----Using lambda---")
    print(print_perms('AB'))

    def find_min_in_rotated_sorted_arr(self, arr: list):
        low, high = 0, len(arr) - 1
        while low < high:
            mid = low + (high - low)//2
            if arr[mid] > arr[high]:
                low = mid + 1
            else:
                high = mid
        return arr[low]

    def binary_search_in_rotated_sorted_arr(self, arr: list, target: int):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = low + (high - low)//2
            if arr[mid] == target:
                return mid
            if arr[low] <= arr[mid]:
                if arr[low] <= target < arr[mid]:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if arr[mid] < target <= arr[high]:
                    low = mid + 1
                else:
                    high = mid - 1
        return -1

    def binary_search_in_sorted_arr(self, arr: list, target: int):
        low, high = 0, len(arr) - 1
        while low <= high:
            mid = low + (high - low)//2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def check_availability(self, check_in: str, check_out: str):
        url = 'https://automationintesting.online/api/room?'
        req_api = url + f"checkin={check_in}&checkout={check_out}"
        print(f"Req api = {req_api}")
        response = requests.get(req_api)
        print(f"response = {response}")
        print(f"response status = {response.status_code}")
        assert response.status_code == 200
        data = response.json()

    def check_double_room(self, room_type: str, check_in: str, check_out: str):
        url = f'https://automationintesting.online/reservation/{room_type}?'
        room_req = url + f"checkin={check_in}&checkout={check_out}"
        room_req_resp = requests.get(room_req)
        print(f"response = {room_req_resp} from req = {room_req}")
        print(f"response status code = {room_req_resp.status_code}")
        assert room_req_resp.status_code == 200

    def find_second_highest(self, num_list: list):
        unique_elements = []
        max_in_list = 0
        count_list = Counter(num_list)
        for num in num_list:
            if count_list[num] < 2:
                unique_elements.append(num)
        print(unique_elements)
        if len(unique_elements) < 2:
            return "Not enough numbers"
        # max_in_list = sorted(list(num_list))[-1]
        for num in num_list:
            if num > max_in_list:
                max_in_list = num
        return [unique_elements[-2] if max_in_list in unique_elements else unique_elements[-1]]

    def read_csv(self, file_path: str):
        path = os.path.join(os.getcwd(), file_path)
        with open(path, 'r') as f:
            print(f"Reading as list")
            for line in f:
                print(line.strip())
            print("\n--- Resetting File Pointer ---\n")
            # Rewind the file back to the very first character
            f.seek(0)
            reader = csv.DictReader(f)
            print(f"Reading as dict")
            for row in reader:
                print(row)
            # Rewind the file back to the very first character
            f.seek(0)
            reader = csv.reader(f)
            print(f"Reading as row by row")
            for row in reader:
                print(row)
        df = pd.read_csv(path)
        print(f"Reading using pandas")
        print(df.head())

if __name__ == "__main__":
    print("--- Running Manually ---")
    test_dsa = TestDSA()
    print("---Longest substring and it's length---")
    test_dsa.length_of_longest_substring('bccabcbb')
    print("---Merge sorted array---")
    print(test_dsa.merge_sorted_arrays([2,3,4,5], [1,3,5,6,7]))
    print("---Count error logs as per decreasing order count but alphabetical file name---")
    test_dsa.count_error_logs_decreasing_order_count_alp_name()
    print("---Non repeated no using Counter in O(N)---")
    print(test_dsa.find_non_repeated_nos([1,2,3,4,5,5,3,3,2]))
    print("---Non repeated no using arr.count() in O(N^2)---")
    print(test_dsa.find_non_repeated_numbers([1,2,3,4,5,5,3,3,2]))
    print("---permute using library---  with T.C=O(N)")
    test_dsa.print_permutations('AB')
    print("---find min in rotated sorted array---")
    print(test_dsa.find_min_in_rotated_sorted_arr([5,6,7,8,9,0,1,2,3]))
    print("---binary search in rotated sorted array---")
    print(test_dsa.binary_search_in_rotated_sorted_arr([7,8,9,0,1,2,3,], 2))
    print("---binary search in sorted array---")
    print(test_dsa.binary_search_in_sorted_arr([1,2,3,4,5], 5))
    test_dsa.check_availability('2026-03-25', '2026-03-26')
    test_dsa.check_double_room(2, '2026-03-25', '2026-03-26')
    print(test_dsa.find_second_highest([9,18,21,26,27,29,27,26,29,30]))
    print(test_dsa.find_second_highest([9,18,21,26,27,29,27,26,29,30,30]))
    print(test_dsa.find_second_highest([9,18,21,26,27,29,27,26,30,30]))
    print(test_dsa.find_second_highest([9,18,21,26,29,29,27,26,30]))
    test_dsa.read_csv(file_path="../helpers/records.csv")
