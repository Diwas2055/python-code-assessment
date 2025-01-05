def length_of_longest_substring(s: str) -> int:
    char_index_map = {}
    max_length = 0
    start = 0

    for end, char in enumerate(s):
        if char in char_index_map and char_index_map[char] >= start:
            start = char_index_map[char] + 1

        char_index_map[char] = end
        max_length = max(max_length, end - start + 1)

    return max_length


# Example usage
input_string = "abcabcbb"
result = length_of_longest_substring(input_string)
print(f"The length of the longest substring without repeating characters is: {result}")
