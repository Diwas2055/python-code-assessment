import hashlib
import base64

url_mapping = {}

BASE62_ALPHABET = base64.b64encode(bytes(range(256))).decode()


def encode_base62(number: int) -> str:
    """Convert an integer to a Base62 string."""
    base62 = []
    while number > 0:
        base62.append(BASE62_ALPHABET[number % 62])
        number //= 62
    return "".join(reversed(base62))


def shorten_url(long_url: str) -> str:
    """Generate a unique short URL."""
    hash_object = hashlib.md5(long_url.encode())
    hash_int = int(hash_object.hexdigest(), 16)

    short_url = encode_base62(hash_int % 62**6)
    return short_url


def add_url_mapping(short_url: str, long_url: str):
    """Store the short URL and its corresponding long URL."""
    url_mapping[short_url] = long_url


def get_long_url(short_url: str) -> str:
    """Retrieve the long URL for a given short URL."""
    return url_mapping.get(short_url, None)


def main():
    while True:
        print("\nURL Shortener")
        print("1. Shorten a URL")
        print("2. Redirect (resolve) a short URL")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            long_url = input("Enter the long URL: ")
            short_url = shorten_url(long_url)
            add_url_mapping(short_url, long_url)
            print(f"Short URL: http://short.ly/{short_url}")

        elif choice == "2":
            short_url = input("Enter the short URL: ").replace("http://short.ly/", "")
            long_url = get_long_url(short_url)

            if long_url:
                print(f"Redirecting to: {long_url}")
            else:
                print("Short URL not found.")

        elif choice == "3":
            print("Exiting the URL shortener service.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
