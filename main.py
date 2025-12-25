import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('users.csv')

# First 3 rows
print(df.head(3))

# increase by 200
print("After increasing")
df.loc[:2, "salary"] = df.loc[:2, "salary"] + 200
print(df.head(3))

# Dataset structure
print(df.info())

# Statistical summary
print(df.describe())

df["age"] = df["age"].fillna(df["age"].mean())
df["salary"] = df["salary"].fillna(df["salary"].mean())

# Check missing values per column
print(df.isnull().sum())

result = df.groupby("country").agg(
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    user_count=("id", "count")
)

print(result)

filtered = df[df["age"] > 30]

avg_salary_30_plus = (
    filtered.groupby("country")["salary"].mean()
)

print("AVG age > 30")
print(avg_salary_30_plus)

plt.figure()
avg_salary_30_plus.plot(kind="bar")
plt.title("Average salary per country")
plt.xlabel("Country")
plt.ylabel("Average salary")
plt.show()

