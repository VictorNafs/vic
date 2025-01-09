import os

original_size = os.path.getsize("img2.png")
converted_size = os.path.getsize("img2.myft")

print(f"Taille originale : {original_size} octets")
print(f"Taille convertie : {converted_size} octets")
reduction = (1 - converted_size / original_size) * 100
print(f"Réduction de taille : {reduction:.2f}%")
