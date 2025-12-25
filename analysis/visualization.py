import pandas as pd
import matplotlib.pyplot as plt

tasks = pd.read_csv("./../data/clean_tasks.csv")

# Task status distribution
status_counts = tasks["status"].value_counts()

plt.figure()
status_counts.plot(kind="bar")
plt.title("Task Status Distribution")
plt.xlabel("Status")
plt.ylabel("Number of Tasks")
plt.show()

# Task duration distribution
plt.figure()
tasks["task_duration_hours"].dropna().plot(kind="hist", bins=10)
plt.title("Task Duration Distribution")
plt.xlabel("Hours")
plt.ylabel("Frequency")
plt.show()