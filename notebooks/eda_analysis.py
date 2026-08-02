import pandas as pd

df = pd.read_csv("../data/Atlantic_France.csv")

print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df["album_type"].value_counts())
print(df["is_explicit"].value_counts())

# --- Clean and prepare ---
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
df["duration_min"] = df["duration_ms"] / 60000
df["album_type"] = df["album_type"].str.lower().str.strip()
df.loc[df["album_type"] == "compilation", "album_type"] = "album"
df["is_explicit"] = df["is_explicit"].astype(bool)

print(df[["date", "duration_min", "album_type"]].head())

# --- Derived features ---
bins = [0, 1, 5, 15, 30, 1000]
labels = ["Single (1)", "EP (2-5)", "Small Album (6-15)", "Large Album (16-30)", "Mega (30+)"]
df["album_size_bucket"] = pd.cut(df["total_tracks"], bins=bins, labels=labels)

dbins = [0, 2.5, 3.5, 4.5, 100]
dlabels = ["Short (<2.5m)", "Medium (2.5-3.5m)", "Long (3.5-4.5m)", "Very Long (4.5m+)"]
df["duration_bucket"] = pd.cut(df["duration_min"], bins=dbins, labels=dlabels)

df["rank_weight"] = 51 - df["position"]

print(df["album_size_bucket"].value_counts())
print(df["duration_bucket"].value_counts())
# --- 1. Explicit content analysis ---
print("\n=== EXPLICIT SHARE ===")
print(df["is_explicit"].value_counts(normalize=True) * 100)

print("\n=== POPULARITY: explicit vs clean ===")
print(df.groupby("is_explicit")["popularity"].mean())

print("\n=== EXPLICIT SHARE BY RANK TIER ===")
for lo, hi, label in [(1, 10, "Top10"), (1, 25, "Top25"), (1, 50, "Top50")]:
    sub = df[(df["position"] >= lo) & (df["position"] <= hi)]
    print(label, sub["is_explicit"].mean() * 100)

# --- 2. Format preference analysis ---
print("\n=== ALBUM TYPE SHARE ===")
print(df["album_type"].value_counts(normalize=True) * 100)

print("\n=== POPULARITY BY ALBUM TYPE ===")
print(df.groupby("album_type")["popularity"].mean())

# --- 3. Album structure impact ---
print("\n=== POPULARITY BY ALBUM SIZE BUCKET ===")
print(df.groupby("album_size_bucket", observed=True)["popularity"].mean())

print("\nCorrelation total_tracks vs popularity:", df["total_tracks"].corr(df["popularity"]))

# --- 4. Duration analysis ---
print("\n=== POPULARITY BY DURATION BUCKET ===")
print(df.groupby("duration_bucket", observed=True)["popularity"].mean())

print("\nCorrelation duration vs popularity:", df["duration_min"].corr(df["popularity"]))
# --- KPI Summary ---
explicit_share = df["is_explicit"].mean() * 100
clean_dom_ratio = (~df["is_explicit"]).sum() / df["is_explicit"].sum()
single_album_ratio = (df["album_type"] == "single").sum() / (df["album_type"] == "album").sum()
avg_duration = df["duration_min"].mean()
album_size_corr = df["total_tracks"].corr(df["popularity"])

w_explicit = df.loc[df["is_explicit"], "rank_weight"].sum()
w_clean = df.loc[~df["is_explicit"], "rank_weight"].sum()
content_acceptance = w_clean / (w_explicit + w_clean) * 100

print("\n=== KPI SUMMARY ===")
print(f"Explicit Content Share:        {explicit_share:.1f}%")
print(f"Clean Dominance Ratio:         {clean_dom_ratio:.2f} : 1")
print(f"Single : Album Ratio:          {single_album_ratio:.2f} : 1")
print(f"Average Song Duration:         {avg_duration:.2f} min")
print(f"Album Size Impact Index:       {album_size_corr:.2f}")
print(f"Clean Content Acceptance Score:{content_acceptance:.1f}%")