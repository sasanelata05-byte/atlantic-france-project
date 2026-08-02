import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Atlantic France Top 50 — Content Compliance Dashboard",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# Custom CSS for a cleaner, branded look
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #1c1f26;
        border: 1px solid #2d323b;
        border-radius: 12px;
        padding: 15px 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="stMetricLabel"] { font-size: 13px; color: #9aa4b2; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #ffffff; }
    h1 { color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1c1f26;
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
    }
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_data
def load_data(path="../data/Atlantic_France.csv"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["duration_min"] = df["duration_ms"] / 60000
    df["album_type"] = df["album_type"].str.lower().str.strip()
    df.loc[df["album_type"] == "compilation", "album_type"] = "album"
    df["is_explicit"] = df["is_explicit"].astype(bool)

    bins = [0, 1, 5, 15, 30, 1000]
    labels = ["Single (1)", "EP (2-5)", "Small Album (6-15)", "Large Album (16-30)", "Mega (30+)"]
    df["album_size_bucket"] = pd.cut(df["total_tracks"], bins=bins, labels=labels)

    dbins = [0, 2.5, 3.5, 4.5, 100]
    dlabels = ["Short (<2.5m)", "Medium (2.5-3.5m)", "Long (3.5-4.5m)", "Very Long (4.5m+)"]
    df["duration_bucket"] = pd.cut(df["duration_min"], bins=dbins, labels=dlabels)

    df["rank_weight"] = 51 - df["position"]
    return df

df_full = load_data()

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
st.sidebar.markdown("## 🎛️ Filters")
st.sidebar.markdown("---")

min_date, max_date = df_full["date"].min(), df_full["date"].max()
date_range = st.sidebar.date_input("📅 Date range", value=(min_date, max_date),
                                    min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = min_date, max_date

rank_tier = st.sidebar.radio("🏆 Rank tier", ["Top 10", "Top 25", "Top 50"], index=2)
tier_map = {"Top 10": 10, "Top 25": 25, "Top 50": 50}
max_rank = tier_map[rank_tier]

explicit_filter = st.sidebar.selectbox("🔞 Explicit content", ["All", "Explicit only", "Clean only"])

album_type_filter = st.sidebar.multiselect(
    "💿 Album type", options=sorted(df_full["album_type"].unique()),
    default=sorted(df_full["album_type"].unique())
)

# Apply filters
df = df_full[
    (df_full["date"] >= start_date) & (df_full["date"] <= end_date)
    & (df_full["position"] <= max_rank) & (df_full["album_type"].isin(album_type_filter))
]
if explicit_filter == "Explicit only":
    df = df[df["is_explicit"]]
elif explicit_filter == "Clean only":
    df = df[~df["is_explicit"]]

if df.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.title("🇫🇷 Atlantic — France Top 50 Content Compliance Dashboard")
st.caption(f"Audience Sensitivity & Format Preference Analysis · {df['date'].min().date()} → {df['date'].max().date()} · {rank_tier}")
st.markdown("---")

# ----------------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------------
explicit_share = df["is_explicit"].mean() * 100
clean_dom_ratio = (~df["is_explicit"]).sum() / max(df["is_explicit"].sum(), 1)
single_album_ratio = (df["album_type"] == "single").sum() / max((df["album_type"] == "album").sum(), 1)
avg_duration = df["duration_min"].mean()
album_size_corr = df["total_tracks"].corr(df["popularity"])
w_explicit = df.loc[df["is_explicit"], "rank_weight"].sum()
w_clean = df.loc[~df["is_explicit"], "rank_weight"].sum()
content_acceptance = w_clean / max(w_explicit + w_clean, 1) * 100

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("🔞 Explicit Share", f"{explicit_share:.1f}%")
k2.metric("✅ Clean Ratio", f"{clean_dom_ratio:.2f}:1")
k3.metric("🎵 Single:Album", f"{single_album_ratio:.2f}:1")
k4.metric("⏱️ Avg Duration", f"{avg_duration:.2f} min")
k5.metric("💿 Size Impact", f"{album_size_corr:.2f}")
k6.metric("📊 Clean Acceptance", f"{content_acceptance:.1f}%")

st.markdown("---")

# ----------------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🔞 Explicit vs Clean", "💿 Format & Album Size", "⏱️ Duration", "📋 Summary"])

PALETTE = {"Explicit": "#E4572E", "Clean": "#17BEBB"}

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        share_df = df["is_explicit"].map({True: "Explicit", False: "Clean"}).value_counts().reset_index()
        share_df.columns = ["Content Type", "Count"]
        fig = px.pie(share_df, names="Content Type", values="Count", hole=0.55,
                     color="Content Type", color_discrete_map=PALETTE,
                     title="Explicit vs Clean — Chart Share")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        pop_df = df.groupby(df["is_explicit"].map({True: "Explicit", False: "Clean"}))["popularity"].mean().reset_index()
        pop_df.columns = ["Content Type", "Avg Popularity"]
        fig = px.bar(pop_df, x="Content Type", y="Avg Popularity", color="Content Type",
                     color_discrete_map=PALETTE, title="Average Popularity", text_auto=".1f")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    rank_explicit = df.groupby("position")["is_explicit"].mean().reset_index()
    rank_explicit["explicit_pct"] = rank_explicit["is_explicit"] * 100
    fig = px.area(rank_explicit, x="position", y="explicit_pct",
                   labels={"position": "Chart Position", "explicit_pct": "% Explicit"},
                   title="Explicit Content Density by Chart Position")
    fig.update_traces(line_color="#E4572E", fillcolor="rgba(228,87,46,0.3)")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fmt_df = df["album_type"].value_counts().reset_index()
        fmt_df.columns = ["Album Type", "Count"]
        fig = px.pie(fmt_df, names="Album Type", values="Count", hole=0.55, title="Single vs Album Share")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        pop_fmt = df.groupby("album_type")["popularity"].mean().reset_index()
        fig = px.bar(pop_fmt, x="album_type", y="popularity", title="Avg Popularity by Format", text_auto=".1f")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    size_pop = df.groupby("album_size_bucket", observed=True)["popularity"].mean().reset_index()
    fig = px.bar(size_pop, x="album_size_bucket", y="popularity",
                 title="Album Structure Impact — Popularity by Album Size", text_auto=".1f",
                 color="popularity", color_continuous_scale="Tealrose")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df, x="duration_min", nbins=40, title="Duration Distribution (min)",
                            color_discrete_sequence=["#17BEBB"])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        dur_pop = df.groupby("duration_bucket", observed=True)["popularity"].mean().reset_index()
        fig = px.bar(dur_pop, x="duration_bucket", y="popularity", title="Popularity by Duration Bucket",
                     text_auto=".1f", color="popularity", color_continuous_scale="Purples")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("📋 Content Compliance Summary")
    col1, col2 = st.columns(2)
    with col1:
        if explicit_share > 55:
            st.error(f"High explicit exposure: {explicit_share:.1f}% of chart slots.")
        else:
            st.success(f"Explicit exposure: {explicit_share:.1f}%.")
        st.info(f"Single:Album ratio is {single_album_ratio:.2f}:1")
    with col2:
        if album_size_corr < -0.2:
            st.warning(f"Album size correlates negatively with popularity ({album_size_corr:.2f}) — dilution effect present.")
        else:
            st.success(f"Weak album-size dilution effect ({album_size_corr:.2f}).")
        st.info(f"Average track duration: {avg_duration:.2f} min")

    st.markdown("### 🎤 Top Artists")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top Explicit Artists**")
        st.dataframe(df[df["is_explicit"]]["artist"].value_counts().head(10).rename("Count"))
    with c2:
        st.markdown("**Top Clean Artists**")
        st.dataframe(df[~df["is_explicit"]]["artist"].value_counts().head(10).rename("Count"))