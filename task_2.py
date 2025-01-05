def fizzbuzz(n: int) -> list[str]:
    return [
        (
            "FizzBuzz"
            if i % 15 == 0
            else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i)
        )
        for i in range(1, n + 1)
    ]


# Example usage
n = 30
result = fizzbuzz(n)
print("\n".join(result))
