def format_numbers(numbers):
    if not numbers:
        return ""
    elif len(numbers) == 1:
        return str(numbers[0])
    elif len(numbers) == 2:
        return f"{numbers[0]} and {numbers[1]}"
    else:
        return f"{', '.join(map(str, numbers[:-1]))}, and {numbers[-1]}"

# Examples
numbers1 = [1]
numbers2 = [1, 2]
numbers3 = [1, 2, 3]
numbers4 = [1, 2, 3, 4]

print(format_numbers(numbers1))  # Output: "1"
print(format_numbers(numbers2))  # Output: "1 and 2"
print(format_numbers(numbers3))  # Output: "1, 2, and 3"
print(format_numbers(numbers4))  # Output: "1, 2, 3, and 4"
