
import csv
from faker import Faker
import random

fake = Faker()

def generate_fake_data():
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = random.choice(["Male", "Female"])
    age = random.randint(18, 90)
    weight = round(random.uniform(40, 120), 2)
    height = round(random.uniform(140, 200), 2)
    health_history = f"HealthHistory{random.randint(1, 100)}"
    return [first_name, last_name, gender, age, weight, height, health_history]

def generate_fake_csv(file_path, num_rows):
    headers = ["first_name", "last_name", "gender", "age", "weight", "height", "health_history"]

    with open(file_path, mode="w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for _ in range(num_rows):
            fake_data = generate_fake_data()
            writer.writerow(fake_data)

if __name__ == "__main__":
    generate_fake_csv("fake_health_care_data.csv", 100)
