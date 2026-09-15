import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load RFM data
rfm = pd.read_csv("rfm_data.csv")

print("RFM data loaded successfully!")
print("Shape:", rfm.shape)

# Select RFM features
rfm_features = rfm[["recency", "frequency", "monetary"]]

# Standardize RFM features
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_features)

print("RFM data standardized successfully!")

# Apply K-Means
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["cluster"] = kmeans.fit_predict(rfm_scaled)

print("\nK-Means clustering completed!")

# Check number of customers in each cluster
print("\nCustomers per cluster:")
print(rfm["cluster"].value_counts().sort_index())

# Calculate cluster profiles
cluster_profile = rfm.groupby("cluster").agg(
    customers=("customer_unique_id", "count"),
    avg_recency=("recency", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary=("monetary", "mean")
).round(2)

print("\nCluster Profiles:")
print(cluster_profile)



rfm.to_csv("customer_segments.csv", index=False)

print("\nCustomer segmentation saved successfully!")
print("File: customer_segments.csv")