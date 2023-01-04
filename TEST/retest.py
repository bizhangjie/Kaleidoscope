import re


text = "The quick brown fox jumps over the lazy dog."

# Use a regular expression to search for a pattern
pattern = r"(\b\w+)\b"
match = re.search(pattern, text)

# Print the matched text
print(match.group(0))
print(match.group(1))