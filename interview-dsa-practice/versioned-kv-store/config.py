from typing import List

def first_pass_config(configs: List[str]) -> int:
    low = 0
    high = len(configs) - 1
    ans = -1

    while low <= high:
        mid = low + (high - low) // 2

        if configs[mid] == 'Pass':
            high = mid - 1
            ans = mid
        else:
            low = mid + 1

    return ans

def get_free_intervals(schedules: List[List[int]], maintenance: List[int]) -> List[List[int]]:
    flattened: List[List[int]] = [i for service in schedules for i in service]
    flattened.sort(key=lambda service: service[0])

    if not flattened:
        return [maintenance]
    
    result: List[List[int]] = []
    start = flattened[0][0]
    end = flattened[0][1]
    
    if start >= maintenance[0] and start <= maintenance[1]:
        result.append([maintenance[0], start])

    if start >= maintenance[1]:
        result.append(maintenance)
    
    for index in range(1, len(flattened)):
        schedule = flattened[index]
        if schedule[0] > end:
            if end >= maintenance[0] and end <= maintenance[1] and schedule[0] >= maintenance[0] and schedule[0] <= maintenance[1]:
                result.append([end, schedule[0]])
            start = schedule[0]
            end = schedule[1]
        else:
            start = min(start, schedule[0])
            end = max(end, schedule[1])
    
    if end >= maintenance[0] and end <= maintenance[1]:  # After for loop ends
        result.append([end, maintenance[1]])
    
    return result

def k_sum(nums: List[int], k: int, target: int) -> List[List[int]]:
    result: List[List[int]] = []
    nums.sort()
    k_sum_rec(nums, k, 0, target, [], result)
    return result

def k_sum_rec(nums: List[int], k: int, start: int, target: int, path: List[int], result: List[List[int]]):
    n = len(nums)

    if k == 2:
        left = start
        right = n - 1

        while left < right:
            sum = nums[left] + nums[right]

            if sum == target:
                result.append(path + [nums[left], nums[right]])
                left += 1
                right -= 1

                while left < right and nums[left] == nums[left - 1]:
                    left += 1

                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

            elif sum < target:
                left += 1

            else:
                right -= 1

        return

    for index in range(start, n - k + 1):
        if index > start and nums[index] == nums[index - 1]:
            continue

        path.append(nums[index])

        k_sum_rec(nums, k - 1, index + 1, target - nums[index], path, result)

        path.pop()

   
