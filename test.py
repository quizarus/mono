def func(nums, k):
    maxes = []
    for i, n in enumerate(nums):
        if len(nums[i:i + k]) < k:
            break
        maxes.append(max(nums[i:i + k]))
    return maxes

def func2(nums, k):
    maxes = []


print(func([6,2,3,7,0,1], 3))


