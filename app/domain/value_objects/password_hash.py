from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordHash:
    value: str

    def __post_init__(self):
        if len(self.value) < 10:  # bcrypt hashes siempre > 50 chars
            raise ValueError("Invalid password hash")
