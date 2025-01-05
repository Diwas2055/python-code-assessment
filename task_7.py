from collections import Counter


def minWindow(s, t):
    if not s or not t or len(s) < len(t):
        return ""

    t_count = Counter(t)
    window_count = Counter()

    left, right = 0, 0
    required = len(t_count)
    formed = 0
    min_len = float("inf")
    min_window = ""

    while right < len(s):
        char = s[right]
        window_count[char] += 1

        if char in t_count and window_count[char] == t_count[char]:
            formed += 1

        while left <= right and formed == required:
            char = s[left]
            window_len = right - left + 1

            if window_len < min_len:
                min_len = window_len
                min_window = s[left : right + 1]

            window_count[char] -= 1
            if char in t_count and window_count[char] < t_count[char]:
                formed -= 1

            left += 1

        right += 1

    return min_window
