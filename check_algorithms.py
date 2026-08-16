def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1
        while j >= 0 and records[j][key] > current[key]:
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = current

def binary_search(sorted_records, target_value, key):
    low = 0
    high = len(sorted_records) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_records[mid][key] == target_value:
            return mid
        elif sorted_records[mid][key] < target_value:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def linear_search(records, target_value, key):
    for i, record in enumerate(records):
        if record[key] == target_value:
            return i
    return -1

def check(name, condition):
    if condition:
        print(f"PASS: {name}")
    else:
        print(f"FAIL: {name}")

# Tests
records = []
insertion_sort(records, "value")
check("insertion_sort empty list", records == [])

records = [{"value": 5}]
insertion_sort(records, "value")
check("insertion_sort single element", records == [{"value": 5}])

data = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}]
check("binary_search first", binary_search(data, 1, "id") == 0)
check("binary_search middle", binary_search(data, 3, "id") == 2)
check("binary_search last", binary_search(data, 5, "id") == 4)
check("binary_search not found", binary_search(data, 99, "id") == -1)
check("linear_search found", linear_search(data, 4, "id") == 3)
check("linear_search not found", linear_search(data, 99, "id") == -1)

print("\nAll checks completed.")