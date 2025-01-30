
from policy.models import Policy
import random


def generate_policy():
    for i in range(1, 100):
        Policy.objects.create(
            name=f"Policy {i}",
            premium=random.randint(1, 10) * 1000,
            coverage=random.randint(1, 100) * 1000,
            type=random.choice(Policy.TYPE_CHOICES)[0],
        )


if __name__ == "__main__":
    generate_policy()

