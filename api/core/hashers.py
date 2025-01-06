from django.contrib.auth.hashers import Argon2PasswordHasher


class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = 8
    memory_cost = 4710
    parallelism = 2
    salt_entropy = 128
