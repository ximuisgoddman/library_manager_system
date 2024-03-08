def max_increasing_subsequence(nums):
    n = len(nums)
    if n == 0:
        return []

    # dp[i] 表示以 nums[i] 结尾的最大递增子序列的长度
    dp = [1] * n

    # 记录最大递增子序列的长度和结束位置
    max_length = 1
    end_index = 0

    # 动态规划求解最大递增子序列的长度
    for i in range(1, n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                if dp[i] > max_length:
                    max_length = dp[i]
                    end_index = i

    # 回溯查找最大递增子序列
    max_subsequence = []
    max_subsequence.append(nums[end_index])
    for i in range(end_index - 1, -1, -1):
        if nums[i] < nums[end_index] and dp[i] == dp[end_index] - 1:
            max_subsequence.append(nums[i])
            end_index = i

    return max_subsequence[::-1]

# 示例用法
nums = [1, 3, 5, 2, 4, 6, 8]
print("最大递增子序列:", max_increasing_subsequence(nums))
