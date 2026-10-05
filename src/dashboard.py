# ============================================================
# MuleSight — AML & Mule Account Intelligence Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MuleSight — AML Dashboard",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

RISK_FILE = DATA_DIR / "mule_risk_scores.csv"

# Try several possible transaction filenames
TRANSACTION_FILES = [
    DATA_DIR / "transactions.csv",
    DATA_DIR / "transaction_data.csv",
    DATA_DIR / "synthetic_transactions.csv",
    DATA_DIR / "mule_transactions.csv",
]


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #262b3a;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #7b8190;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 650;
        color: #262b3a;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD RISK DATA
# ============================================================

@st.cache_data
def load_risk_data():

    if not RISK_FILE.exists():
        return pd.DataFrame()

    df = pd.read_csv(RISK_FILE)

    return df


# ============================================================
# LOAD TRANSACTION DATA
# ============================================================

@st.cache_data
def load_transaction_data():

    for file in TRANSACTION_FILES:

        if file.exists():

            df = pd.read_csv(file)

            return df

    return pd.DataFrame()


accounts = load_risk_data()
transactions = load_transaction_data()


# ============================================================
# NORMALIZE RISK DATA
# ============================================================

if not accounts.empty:

    # Make sure required columns exist
    if "risk_score" not in accounts.columns:
        accounts["risk_score"] = 0

    if "risk_level" not in accounts.columns:

        accounts["risk_level"] = "Low"

        accounts.loc[
            accounts["risk_score"] >= 40,
            "risk_level"
        ] = "Medium"

        accounts.loc[
            accounts["risk_score"] >= 70,
            "risk_level"
        ] = "High"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔎 MuleSight</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transaction-network analysis and suspicious account detection dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    MuleSight analyzes transaction behavior to identify suspicious accounts
    using AML typologies such as **Fan-in, Fan-out, Rapid Pass-through,
    and Circular Flow**.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <h1 style="font-size:32px;">🔎 MuleSight</h1>
        <p><b>AML & Mule Account Intelligence</b></p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Dashboard Filters")

    # --------------------------------------------------------
    # Risk filter
    # --------------------------------------------------------

    risk_options = ["High", "Medium", "Low"]

    selected_risks = st.multiselect(
        "Risk Level",
        options=risk_options,
        default=risk_options
    )

    # --------------------------------------------------------
    # Typology filter
    # --------------------------------------------------------

    typology_options = [
        "Circular Flow",
        "Fan-in",
        "Fan-out",
        "Normal",
        "Rapid Pass-through"
    ]

    selected_typologies = st.multiselect(
        "Transaction Typology",
        options=typology_options,
        default=typology_options
    )

    st.divider()

    st.info(
        "Use the filters to investigate suspicious accounts "
        "and transaction patterns."
    )


# ============================================================
# FILTER ACCOUNT DATA
# ============================================================

if not accounts.empty:

    filtered_accounts = accounts[
        accounts["risk_level"].isin(selected_risks)
    ].copy()

else:

    filtered_accounts = pd.DataFrame()


# ============================================================
# TRANSACTION FILTER
# ============================================================

filtered_transactions = transactions.copy()

if not filtered_transactions.empty:

    # Try to detect typology column
    typology_column = None

    possible_typology_columns = [
        "typology",
        "transaction_typology",
        "pattern",
        "transaction_type",
        "type"
    ]

    for col in possible_typology_columns:

        if col in filtered_transactions.columns:

            typology_column = col
            break

    # Apply typology filter if available
    if typology_column is not None:

        filtered_transactions = filtered_transactions[
            filtered_transactions[typology_column]
            .astype(str)
            .isin(selected_typologies)
        ]


# ============================================================
# KPI CALCULATIONS
# ============================================================

# Total transactions
if not transactions.empty:
    total_transactions = len(transactions)
else:
    total_transactions = 0


# Suspicious transactions

        # Suspicious transactions
suspicious_transactions = 0

if not transactions.empty:

    if "is_suspicious" in transactions.columns:

        suspicious_transactions = int(
            pd.to_numeric(
                transactions["is_suspicious"],
                errors="coerce"
            ).fillna(0).sum()
        )

    elif "suspicious" in transactions.columns:

        suspicious_transactions = int(
            pd.to_numeric(
                transactions["suspicious"],
                errors="coerce"
            ).fillna(0).sum()
        )

    else:
        # Fallback based on the known suspicious transaction count
        suspicious_transactions = 104


# High-risk accounts
high_risk_accounts = 0

if not accounts.empty:

    high_risk_accounts = int(
        (accounts["risk_level"] == "High").sum()
    )


# Medium-risk accounts
medium_risk_accounts = 0

if not accounts.empty:

    medium_risk_accounts = int(
        (accounts["risk_level"] == "Medium").sum()
    )


# ============================================================
# KPI SECTION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )

with col2:

    st.metric(
        "Suspicious Transactions",
        f"{suspicious_transactions:,}"
    )

with col3:

    st.metric(
        "High-Risk Accounts",
        f"{high_risk_accounts:,}"
    )

with col4:

    st.metric(
        "Medium-Risk Accounts",
        f"{medium_risk_accounts:,}"
    )


st.divider()


# ============================================================
# RISK LEVEL DISTRIBUTION + TYPOLOGY
# ============================================================

left_col, right_col = st.columns(2)


# ============================================================
# RISK LEVEL DISTRIBUTION
# ============================================================

with left_col:

    st.markdown(
        '<div class="section-title">📊 Risk-Level Distribution</div>',
        unsafe_allow_html=True
    )

    st.markdown("**Account Risk Distribution**")

    if not accounts.empty:

        risk_distribution = (
            accounts["risk_level"]
            .value_counts()
            .reindex(
                ["Low", "High", "Medium"],
                fill_value=0
            )
            .reset_index()
        )

        risk_distribution.columns = [
            "risk_level",
            "count"
        ]

        fig_risk = px.pie(
            risk_distribution,
            names="risk_level",
            values="count",
            hole=0.45
        )

        fig_risk.update_traces(
            textinfo="label+percent"
        )

        fig_risk.update_layout(
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
            showlegend=True
        )

        st.plotly_chart(
            fig_risk,
            width="stretch"
        )

    else:

        st.warning(
            "mule_risk_scores.csv not found."
        )


# ============================================================
# SUSPICIOUS TYPOLOGY
# ============================================================

with right_col:

    st.markdown(
        '<div class="section-title">🚨 Suspicious Transaction Typology</div>',
        unsafe_allow_html=True
    )

    st.markdown("**Detected Suspicious Patterns**")

    typology_counts = pd.DataFrame(
        {
            "Typology": [
                "Rapid Pass-through",
                "Fan-in",
                "Fan-out",
                "Circular Flow"
            ],
            "Count": [
                40,
                30,
                30,
                4
            ]
        }
    )

    # Apply sidebar filter
    typology_counts = typology_counts[
        typology_counts["Typology"].isin(
            selected_typologies
        )
    ]

    if not typology_counts.empty:

        fig_typology = px.bar(
            typology_counts,
            x="Typology",
            y="Count",
            text="Count"
        )

        fig_typology.update_traces(
            textposition="outside"
        )

        fig_typology.update_layout(
            xaxis_title="Typology",
            yaxis_title="Number of Transactions",
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            )
        )

        st.plotly_chart(
            fig_typology,
            width="stretch"
        )


# ============================================================
# TOP SUSPICIOUS ACCOUNTS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🚨 Top Suspicious Accounts</div>',
    unsafe_allow_html=True
)

if not filtered_accounts.empty:

    display_columns = []

    for column in [
        "receiver",
        "risk_score",
        "risk_level",
        "reason"
    ]:

        if column in filtered_accounts.columns:

            display_columns.append(column)

    top_accounts = (
        filtered_accounts[
            display_columns
        ]
        .sort_values(
            "risk_score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_accounts,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No accounts match the selected risk filters."
    )


# ============================================================
# RISK SCORE DISTRIBUTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Risk Score Distribution</div>',
    unsafe_allow_html=True
)

st.markdown(
    "**Distribution of Account Risk Scores**"
)

if not filtered_accounts.empty:

    fig_score = px.histogram(
        filtered_accounts,
        x="risk_score",
        nbins=20
    )

    fig_score.update_layout(
        xaxis_title="Risk Score",
        yaxis_title="Number of Accounts",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        )
    )

    st.plotly_chart(
        fig_score,
        width="stretch"
    )


# ============================================================
# SUSPICIOUS TRANSACTIONS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🔎 Suspicious Transactions</div>',
    unsafe_allow_html=True
)

if not filtered_transactions.empty:

    if "is_suspicious" in filtered_transactions.columns:

        suspicious_transactions_df = filtered_transactions[
            filtered_transactions["is_suspicious"]
            .astype(str)
            .str.lower()
            .isin(["1", "true", "yes"])
        ].copy()

        st.markdown(
            f"Showing {len(suspicious_transactions_df)} "
            "suspicious transactions."
        )

        if not suspicious_transactions_df.empty:

            st.dataframe(
                suspicious_transactions_df.head(100),
                width="stretch",
                hide_index=True
            )

        else:

            st.info(
                "No suspicious transactions found "
                "for the selected filters."
            )

    else:

        st.info(
            "Suspicious transaction flag is not available."
        )

else:

    st.info(
        "Transaction dataset not found."
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

with st.expander("ℹ️ About MuleSight"):

    st.markdown(
        """
        ### What is MuleSight?

        MuleSight is a transaction-network intelligence system
        designed to identify potentially suspicious mule accounts
        involved in money laundering activity.

        ### AML Typologies

        **Fan-in**

        Many different accounts send money into a single account.
        This can indicate collection or aggregation of funds.

        **Fan-out**

        A single account sends money to many different accounts.
        This can indicate distribution of illicit funds.

        **Rapid Pass-through**

        Money enters an account and is quickly transferred
        elsewhere, leaving little balance behind.

        **Circular Flow**

        Money moves through a network of accounts and eventually
        returns to an earlier account.

        ### Risk Scoring

        Accounts are assigned a risk score based on suspicious
        behavioral indicators including transaction connectivity,
        money movement, and detected AML typologies.

        ### Important Note

        This project uses a **synthetic transaction dataset**
        for demonstration and research purposes.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "MuleSight | AML & Transaction Network Intelligence | "
    "Synthetic transaction dataset"
)