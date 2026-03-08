import pandas as pd

# Load the dataset
data = pd.read_csv("../data/service_requests.csv", header=None, encoding="utf-8-sig")

# If the whole row is loaded into one column, split it manually by comma
if data.shape[1] == 1:
    data = data[0].str.split(",", expand=True)

# Use first row as header
data.columns = data.iloc[0].str.strip()
data = data[1:].reset_index(drop=True)

# Clean column names
data.columns = data.columns.str.strip()

# Debug: show column names
print(data.columns.tolist())

# Define which statuses are still open
open_statuses = ["New Request", "Price Requested", "Waiting Technician", "Under Review"]

# Filter urgent requests:
# High priority + still open
urgent_requests = data[
    (data["Priority"] == "High") &
    (data["Status"].isin(open_statuses))
]

# Print summary
print("Urgent Service Request Summary")
print("------------------------------")
print(f"Total urgent open requests: {len(urgent_requests)}\n")

for _, row in urgent_requests.iterrows():
    print(
        f"{row['Request_ID']} | {row['Company']} | "
        f"{row['Status']} | Follow-up: {row['Next_Followup_Date']}"
    )

# Save urgent requests to a new CSV file
urgent_requests.to_csv("../data/urgent_requests.csv", index=False)

print("\nA filtered file has been saved as: urgent_requests.csv")
