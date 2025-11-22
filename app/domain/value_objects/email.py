from dataclasses import dataclass
import re

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(EMAIL_REGEX, self.value):
            raise ValueError("Invalid email format")
