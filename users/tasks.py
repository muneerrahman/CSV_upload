from celery import shared_task
from .models import ImportedUser
import csv
from io import StringIO

@shared_task
def process_csv_data(file_data):
    decoded_file = StringIO(file_data)
    reader = csv.DictReader(decoded_file)
    success_count = 0
    failed = []

    for row in reader:
        name = row.get('name')
        email = row.get('email')
        try:
            age = int(row.get('age', -1))
        except:
            age = -1

        if not (name and email and 0 <= age <= 120):
            failed.append({"email": email, "reason": "invalid data"})
            continue

        if ImportedUser.objects.filter(email=email).exists():
            failed.append({"email": email, "reason": "Duplicate email"})
            continue

        ImportedUser.objects.create(name=name, email=email, age=age)
        success_count += 1

    return {"success_count": success_count, "failed": failed}
