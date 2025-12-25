import pandas as pd

# Load datasets
users = pd.read_csv("./../data/users.csv")
tasks = pd.read_csv("./../data/tasks.csv")
events = pd.read_csv("./../data/events.csv")
ab = pd.read_csv("./../data/ab_test_results.csv")

# Convert date columns
users["signup_date"] = pd.to_datetime(users["signup_date"])
tasks["created_at"] = pd.to_datetime(tasks["created_at"])
tasks["completed_at"] = pd.to_datetime(tasks["completed_at"], errors="coerce")
events["event_date"] = pd.to_datetime(events["event_date"])

# Create task duration (hours)
tasks["task_duration_hours"] = (
    tasks["completed_at"] - tasks["created_at"]
).dt.total_seconds() / 3600

# Save cleaned datasets
users.to_csv("./../data/clean_users.csv", index=False)
tasks.to_csv("./../data/clean_tasks.csv", index=False)
events.to_csv("./../data/clean_events.csv", index=False)
ab.to_csv("./../data/clean_ab_test_results.csv", index=False)

print("Data cleaning completed")