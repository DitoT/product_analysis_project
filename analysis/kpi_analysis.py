import pandas as pd

# Load Clean ddata
tasks = pd.read_csv("./../data/clean_tasks.csv")
events = pd.read_csv("./../data/clean_events.csv")

# Completion rate
completion_rate = (
    tasks["status"].value_counts(normalize=True).get("completed", 0)
)

# Average task duration
avg_task_duration = tasks["task_duration_hours"].mean()

# Active users
active_users = events["user_id"].unique()

print("KPI RESULTS")
print(f"Completion Rate: {completion_rate:.2%}")
print(f"Average Task Duration (hours): {avg_task_duration:.2f}")
print(f"Active Users: {active_users}")