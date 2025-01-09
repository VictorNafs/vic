import os

original_size = os.path.getsize("example.png")
converted_size = os.path.getsize("example.vic")

print(f"Original size: {original_size} bytes")
print(f"Converted size: {converted_size} bytes")
reduction = (1 - converted_size / original_size) * 100
print(f"Size reduction: {reduction:.2f}%")
