import pandas as pd

ab = pd.read_csv("./../data/clean_ab_test_results.csv")

# Conversion rate per variant
conversion_rates = ab.groupby("variant")["converted"].mean()

print("A/B TEST RESULTS")
print(conversion_rates)

if conversion_rates["B"] > conversion_rates["A"]:
    print("Variant B performs better than Variant A.")
else:
    print("No improvement observed.")