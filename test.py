from typing import List

def maxSumMinProduct(nums: List[int]) -> int:
    MOD = 10 ** 9 + 7
    n = len(nums)

    prefix = [0] * (n + 1)

    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    stack = []
    maxi = 0

    for i in range(n + 1):
        current = nums[i] if i < n else 0

        while stack and nums[stack[-1]] > current:
            min_index = stack.pop()
            min_value = nums[min_index]

            if stack:
                left = stack[-1] + 1
            else:
                left = 0

            right = i - 1

            subarray_sum = prefix[right + 1] - prefix[left]
            maxi = max(maxi, subarray_sum * min_value)

        stack.append(i)

    return maxi % MOD

def main():
    print(maxSumMinProduct([2,3,3,1,2]))

main()