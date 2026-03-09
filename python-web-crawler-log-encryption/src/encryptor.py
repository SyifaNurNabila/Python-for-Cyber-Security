from cryptography.fernet import Fernet

# membuat key
key = Fernet.generate_key()

# simpan key
with open("secret.key", "wb") as key_file:
    key_file.write(key)

# baca file log
with open("outputs/results.log", "rb") as file:
    data = file.read()

# enkripsi data
fernet = Fernet(key)
encrypted = fernet.encrypt(data)

# simpan hasil enkripsi
with open("outputs/results.enc", "wb") as file:
    file.write(encrypted)

print("File berhasil dienkripsi menjadi results.enc")