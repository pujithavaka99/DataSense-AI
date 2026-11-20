import streamlit as st
import pandas as pd
import os

# --------------------------------------------------
# IMPORTS
# --------------------------------------------------

from utils.data_loader import load_dataset
from utils.data_cleaner import clean_data

from utils.data_quality import check_data_quality
from utils.missing_value_analyzer import investigate_missing_totalcharges

from utils.data_insights import (
    calculate_churn_rate,
    analyze_churn_by_contract,
    analyze_churn_by_tenure,
    identify_contract_risk
)

from utils.visualizer import (
    plot_churn_by_contract,
    plot_churn_by_tenure
)

from utils.business_insight_generator import generate_business_insights

from utils.general_analytics import (
    analyze_general_dataset,
    create_general_visualization,
    recommend_chart_type,
    create_correlation_heatmap,
    explain_correlations,
    detect_id_columns
)



from agents.data_quality_agent import DataQualityAgent
from agents.data_analyst_agent import DataAnalystAgent

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DataSense AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM UI STYLING
# --------------------------------------------------

st.markdown("""
<style>

    .stApp {
        background-color: #0E1117;
        color: #E6EDF3;
    }

    h1 {
        color: #58A6FF !important;
        font-weight: 700;
    }

    h2, h3 {
        color: #E6EDF3 !important;
    }

    [data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #8B949E !important;
    }

    [data-testid="stMetricValue"] {
        color: #58A6FF !important;
    }

    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #30363D;
        border-radius: 10px;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: #30363D;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🤖 DataSense AI")

    st.caption("Your Autonomous Data Intelligence Platform")

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "🏠 Overview",
            "🔍 Data Quality",
            "📈 Business Analytics",
            "🧠 AI Insights"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 📁 Dataset")

    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        st.session_state["uploaded_dataset"] = uploaded_file
        st.session_state["dataset_name"] = uploaded_file.name

    else:

        st.session_state["uploaded_dataset"] = None
        st.session_state["dataset_name"] = "IBM Telco Customer Churn"

    st.caption("Upload a CSV to analyze your own data.")

    st.divider()

    st.caption("Powered by Python · Pandas · Plotly · AI")


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

uploaded_file = st.session_state.get("uploaded_dataset")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    dataset_name = uploaded_file.name

    st.sidebar.success("Custom dataset loaded!")

else:

    data_path = "data/Telco-Customer-Churn.csv"

    df = load_dataset(data_path)

    dataset_name = "IBM Telco Customer Churn"

    if df is None:

        st.error("Dataset could not be loaded.")

        st.stop()


# --------------------------------------------------
# INITIALIZE AGENTS
# --------------------------------------------------

data_quality_agent = DataQualityAgent()

data_analyst_agent = DataAnalystAgent()

# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

df = clean_data(df)


# --------------------------------------------------
# DATASET TYPE DETECTION
# --------------------------------------------------

required_telco_columns = [
    "Churn",
    "Contract",
    "tenure"
]

is_telco_dataset = all(
    column in df.columns
    for column in required_telco_columns
)

if is_telco_dataset:

    st.sidebar.success("Telco dataset detected")

else:

    st.sidebar.info("General dataset detected")


# --------------------------------------------------
# ACTIVE DATASET INFORMATION
# --------------------------------------------------

st.sidebar.divider()

st.sidebar.markdown("### 📊 Active Dataset")

st.sidebar.write(dataset_name)

st.sidebar.caption(
    f"{df.shape[0]:,} records · {df.shape[1]} columns"
)


# --------------------------------------------------
# COMMON ANALYTICS
# --------------------------------------------------

if is_telco_dataset:

    churn_insight = calculate_churn_rate(df)

    contract_analysis = analyze_churn_by_contract(df)

    tenure_analysis = analyze_churn_by_tenure(df)

    contract_risk = identify_contract_risk(contract_analysis)

    business_insights = generate_business_insights(
        churn_insight,
        contract_risk,
        contract_analysis,
        tenure_analysis
    )

    general_analysis = None

else:

    churn_insight = None

    contract_analysis = None

    tenure_analysis = None

    contract_risk = None

    business_insights = []

    general_analysis = analyze_general_dataset(df)


# --------------------------------------------------
# DATA QUALITY ANALYSIS
# --------------------------------------------------

quality_report = check_data_quality(df)

if is_telco_dataset:

    missing_report = investigate_missing_totalcharges(df)

else:

    missing_report = None


total_missing = sum(
    quality_report["missing_values"].values()
)

total_duplicates = quality_report["duplicate_rows"]

total_empty_strings = sum(
    quality_report["empty_strings"].values()
)

total_whitespace = sum(
    quality_report["whitespace_values"].values()
)


# --------------------------------------------------
# QUALITY STATUS
# --------------------------------------------------

if (
    total_duplicates == 0
    and total_empty_strings == 0
    and total_whitespace == 0
    and (
        not is_telco_dataset
        or missing_report["positive_tenure_missing"] == 0
    )
):

    quality_status = "GOOD - REVIEWED"

else:

    quality_status = "REQUIRES ATTENTION"



# --------------------------------------------------
# PAGE 1: OVERVIEW
# --------------------------------------------------

if page == "🏠 Overview":

    st.title("📊 Dataset Overview")

    st.caption(
        "Monitor your dataset and understand customer behavior at a glance."
    )

    st.markdown(
        "Explore the dataset and understand the overall "
        "customer churn situation."
    )

    # Dataset metrics

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Rows",
        df.shape[0]
    )

    col2.metric(
        "Total Columns",
        df.shape[1]
    )

    # Dataset size

    if uploaded_file is not None:

        file_size = uploaded_file.size / 1024

    else:

        file_size = os.path.getsize(data_path) / 1024

    col3.metric(
        "Dataset Size",
        f"{file_size:.2f} KB"
    )

    st.divider()

    # Dataset preview

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    # Customer churn overview

    if is_telco_dataset:

        st.subheader("Customer Churn Overview")

        total_customers = churn_insight["total_customers"]

        churned_customers = churn_insight["churned_customers"]

        churn_rate = churn_insight["churn_rate_percentage"]

        retained_customers = (
            total_customers - churned_customers
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Customers",
            total_customers
        )

        col2.metric(
            "Churned Customers",
            churned_customers
        )

        col3.metric(
            "Churn Rate",
            f"{churn_rate}%"
        )

    else:

        st.subheader("Dataset Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Records",
            len(df)
        )

        col2.metric(
            "Total Columns",
            len(df.columns)
        )

        col3.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )

        st.info(
            "Churn-specific metrics are available when "
            "the IBM Telco Customer Churn dataset is loaded."
        )


# --------------------------------------------------
# PAGE 2: DATA QUALITY
# --------------------------------------------------

elif page == "🔍 Data Quality":

    st.title("🔍 Data Quality")

    st.caption(
        "Inspect missing values, duplicates, and data consistency."
    )
    # Run Data Quality Agent

    quality_report = data_quality_agent.run_quality_analysis(df)

    quality_score = quality_report["Data Quality Score"]

    quality_rating = data_quality_agent.get_quality_rating(
        quality_score
    )
    quality_explanation = data_quality_agent.get_quality_explanation(
    quality_score
)
    # Display Data Quality Score

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Data Quality Score",
            f"{quality_score}%"
        )

    with col2:

        st.metric(
            "Quality Rating",
            quality_rating
        )
    st.info(quality_explanation)
    # Generate Data Quality Recommendations

    recommendations = data_quality_agent.generate_recommendations(df)

    # Data Quality Recommendations

    st.subheader("🤖 Agent Recommendations")

    for recommendation in recommendations:

        severity = recommendation["severity"]

        issue = recommendation["issue"]

        message = recommendation["recommendation"]
        with st.expander(f"{severity} — {issue}", expanded=True):
            if severity == "Critical":

                st.error(f"🔴 {issue}: {message}")

            elif severity == "Warning":

                st.warning(f"🟠 {issue}: {message}")

            else:

                st.info(f"🔵 {issue}: {message}")
    # Data Quality Summary
    summary = data_quality_agent.generate_quality_summary(df)
    # Column-Level Data Quality Issues

    st.subheader("🔎 Column-Level Data Quality Issues")

    column_issues = []

    # Missing values
    missing_df = quality_report["Missing Values"]

    for column, row in missing_df.iterrows():

        column_issues.append({
            "Column": column,
            "Issue": "Missing Values",
            "Count": int(row["Missing Count"]),
            "Percentage": f'{row["Missing Percentage"]:.2f}%'
        })

    # Empty strings
    empty_string_analysis = quality_report["Empty String Analysis"]

    for column, count in empty_string_analysis.items():

        percentage = (count / len(df)) * 100 if len(df) > 0 else 0

        column_issues.append({
            "Column": column,
            "Issue": "Empty Strings",
            "Count": count,
            "Percentage": f"{percentage:.2f}%"
        })

    # Constant columns
    constant_columns = quality_report["Constant Columns"]

    for column in constant_columns:

        column_issues.append({
            "Column": column,
            "Issue": "Constant Column",
            "Count": "-",
            "Percentage": "-"
        })

    # Display issues
    if column_issues:

        issues_df = pd.DataFrame(column_issues)

        st.dataframe(
    issues_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Column": st.column_config.TextColumn(
            "Column",
            width="medium"
        ),
        "Issue": st.column_config.TextColumn(
            "Issue",
            width="medium"
        ),
        "Count": st.column_config.NumberColumn(
            "Count",
            width="small"
        ),
        "Percentage": st.column_config.TextColumn(
            "Percentage",
            width="small"
        )
    }
)
    else:

        st.success("No column-level data quality issues detected.")

    st.subheader("📋 Data Quality Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", summary["Total Rows"])

    with col2:
        st.metric("Total Columns", summary["Total Columns"])

    with col3:
        st.metric("Missing Values", summary["Missing Values"])

    with col4:
        st.metric("Duplicate Rows", summary["Duplicate Rows"])

    col5, col6 = st.columns(2)

    with col5:
        st.metric("Empty Strings", summary["Empty Strings"])

    with col6:
        st.metric("Constant Columns", summary["Constant Columns"])
    # Missing values

    missing_values = df.isnull().sum()

    total_missing = int(missing_values.sum())

    # Duplicate rows

    duplicate_rows = int(df.duplicated().sum())

    # Empty strings

    empty_strings = (
        df.astype(str)
        .apply(lambda column: column.str.strip().eq(""))
        .sum()
    )

    total_empty_strings = int(empty_strings.sum())

    # Whitespace-only values

    whitespace_values = (
        df.astype(str)
        .apply(
            lambda column: column.str.fullmatch(
                r"\s+"
            ).fillna(False)
        )
        .sum()
    )

    total_whitespace = int(whitespace_values.sum())

    # Metrics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Missing Values",
        total_missing
    )

    col2.metric(
        "Duplicate Rows",
        duplicate_rows
    )

    col3.metric(
        "Empty Strings",
        total_empty_strings
    )

    col4.metric(
        "Whitespace Values",
        total_whitespace
    )

    st.divider()



    # Data preview

    st.subheader("👀 Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.divider()

    # Data types

    st.subheader("🔤 Column Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(
        dtype_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# PAGE 3: BUSINESS ANALYTICS
# --------------------------------------------------

elif page == "📈 Business Analytics":

    st.title("📈 Business Analytics")

    st.caption(
        "Explore patterns, customer segments, and dataset behavior."
    )

    # ----------------------------------------------
    # TELCO DATASET ANALYTICS
    # ----------------------------------------------

    if is_telco_dataset:

        st.subheader("Churn by Contract Type")

        st.dataframe(
            contract_analysis,
            use_container_width=True
        )

        contract_chart = plot_churn_by_contract(
            contract_analysis
        )

        st.plotly_chart(
            contract_chart,
            use_container_width=True
        )

        st.divider()

        st.subheader("Churn by Customer Tenure")

        st.dataframe(
            tenure_analysis,
            use_container_width=True
        )

        tenure_chart = plot_churn_by_tenure(
            tenure_analysis
        )

        st.plotly_chart(
            tenure_chart,
            use_container_width=True
        )

        st.divider()

        st.subheader("Contract Risk Comparison")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Highest Risk Contract",
            contract_risk["highest_risk_contract"]
        )

        col2.metric(
            "Highest Churn Rate",
            f"{contract_risk['highest_risk_churn_rate']}%"
        )

        col3.metric(
            "Risk Gap",
            f"{contract_risk['risk_gap_percentage_points']} percentage points"
        )

    # ----------------------------------------------
    # GENERAL DATASET ANALYTICS
    # ----------------------------------------------

    else:

        st.subheader("🔢 Numerical Analysis")

        if general_analysis["numerical_columns"]:

            st.dataframe(
                general_analysis["numerical_summary"],
                use_container_width=True
            )

        else:

            st.info(
                "No numerical columns found in this dataset."
            )

        st.divider()

        st.subheader("🏷️ Categorical Analysis")

        if general_analysis["categorical_summary"]:

            categorical_data = pd.DataFrame(
                general_analysis["categorical_summary"]
            ).T

            st.dataframe(
                categorical_data,
                use_container_width=True
            )

        else:

            st.info(
                "No categorical columns found in this dataset."
            )

        st.divider()

        # ------------------------------------------
        # INTERACTIVE VISUALIZATION
        # ------------------------------------------

        st.subheader("📊 Interactive Visualization")

        visualization_columns = (
            general_analysis["numerical_columns"]
            + general_analysis["categorical_columns"]
        )

        # Column label formatter

        def format_column_name(column):

            if column in general_analysis["numerical_columns"]:

                return f"📊 {column} — Numeric"

            unique_count = df[column].nunique()

            total_count = len(df)

            unique_ratio = (
                unique_count / total_count
                if total_count > 0
                else 0
            )

            if unique_ratio > 0.50:

                return (
                    f"📝 {column} — "
                    "High-cardinality categorical"
                )

            return f"🏷️ {column} — Categorical"

        # Check visualization columns

        if visualization_columns:

            selected_column = st.selectbox(
                "Select a column to visualize",
                visualization_columns,
                format_func=format_column_name
            )
            numerical_columns = df.select_dtypes(
                 include="number"
            ).columns.tolist()

            id_columns = detect_id_columns(df)

            numerical_columns = [
                 column for column in numerical_columns
                 if column not in id_columns
            ]
            # Automatic chart recommendation

            recommended_chart, recommendation_reason = (
                recommend_chart_type(
                    df,
                    selected_column
                )
            )

            st.info(
                f"**Recommended Visualization:** "
                f"{recommended_chart}\n\n"
                f"{recommendation_reason}"
            )

            # Create chart

            chart = create_general_visualization(
                df,
                selected_column
            )

            st.plotly_chart(
                chart,
                use_container_width=True
            )
            # Correlation Heatmap
            if len(numerical_columns) >= 2:
                st.subheader("🔗 Correlation Heatmap")

                heatmap = create_correlation_heatmap(
                    df,
                    numerical_columns
                )

                if heatmap is not None:
                    st.plotly_chart(heatmap, use_container_width=True)
            # Correlation Insights
            st.subheader("🧠 Correlation Insights")

            correlation_insights = explain_correlations(
                df,
                numerical_columns
        )

        for insight in correlation_insights:
            st.markdown(f"• {insight}")
       


# --------------------------------------------------
# PAGE 4: AI INSIGHTS
# --------------------------------------------------

elif page == "🧠 AI Insights":

    st.title("🧠 AI Insights")

    st.caption(
        "Business insights, statistical findings, "
        "and actionable recommendations"
    )

    # --------------------------------------------------
    # TELCO BUSINESS INSIGHTS
    # --------------------------------------------------

    if is_telco_dataset:

        st.subheader("📊 Key Business Findings")

        for insight in business_insights:

            st.info(insight)

        st.divider()

        st.subheader("🎯 Business Recommendations")

        recommendations = [
            "Focus retention campaigns on month-to-month customers.",
            "Encourage customers to move toward long-term contracts.",
            "Identify new customers who may be at high risk of churn.",
            "Improve customer engagement during the first 12 months."
        ]

        for recommendation in recommendations:

            st.success(recommendation)

        st.divider()


    # --------------------------------------------------
    # DATA ANALYST AGENT
    # --------------------------------------------------

    st.subheader("🤖 Data Analyst Agent")

    analyst_results = data_analyst_agent.run_analysis(df)


    # --------------------------------------------------
    # KEY FINDINGS
    # --------------------------------------------------

    st.subheader("💡 Key Findings")

    key_findings = analyst_results.get("Key Findings", [])

    if isinstance(key_findings, list):

        for finding in key_findings:

            st.info(finding)

    else:

        st.info(key_findings)

    # --------------------------------------------------
# STATISTICAL INSIGHTS
# --------------------------------------------------

    with st.expander("📈 Statistical Insights", expanded=False):

        statistical_insights = analyst_results.get(
        "Statistical Insights", []
    )

        if isinstance(statistical_insights, list):

            for insight in statistical_insights:

                st.write(f"• {insight}")

        elif isinstance(statistical_insights, str):

            st.write(statistical_insights)


    # --------------------------------------------------
# NUMERICAL ANALYSIS
# --------------------------------------------------

    with st.expander("🔢 Numerical Analysis", expanded=False):

        numerical_analysis = analyst_results.get(
        "Numerical Analysis", {}
        )

        if isinstance(numerical_analysis, dict) and numerical_analysis:

            numerical_df = pd.DataFrame(numerical_analysis).T

            st.dataframe(
                numerical_df,
                use_container_width=True
            )

        else:

            st.info(numerical_analysis)

    # --------------------------------------------------
# CATEGORICAL ANALYSIS
# --------------------------------------------------

    with st.expander("📋 Categorical Analysis", expanded=False):

        categorical_analysis = analyst_results.get(
            "Categorical Analysis", {}
        )

        if isinstance(categorical_analysis, dict) and categorical_analysis:

            categorical_df = pd.DataFrame(
                categorical_analysis
            ).T

            st.dataframe(
            categorical_df,
            use_container_width=True
            )

            for column, details in categorical_analysis.items():

                distribution = details.get(
                    "Value Distribution", {}
                )

                if distribution:

                    with st.expander(
                        f"View distribution of {column}"
                    ):

                        st.write(distribution)

        else:

            st.info(categorical_analysis)


    # --------------------------------------------------
# OUTLIER ANALYSIS
# --------------------------------------------------

    with st.expander("🚨 Outlier Analysis", expanded=False):

        outlier_analysis = analyst_results.get(
            "Outlier Analysis", {}
        )

        if isinstance(outlier_analysis, dict) and outlier_analysis:

            outlier_df = pd.DataFrame(
                outlier_analysis
            ).T

            st.dataframe(
                outlier_df,
                use_container_width=True
            )

        else:

            st.info(outlier_analysis)


    # --------------------------------------------------
# CORRELATION ANALYSIS
# --------------------------------------------------

    with st.expander("🔗 Correlation Analysis", expanded=False):

        correlation_analysis = analyst_results.get(
            "Correlation Analysis", {}
        )

        if isinstance(correlation_analysis, dict) and correlation_analysis:

            correlation_df = pd.DataFrame(
                correlation_analysis
            ).T

            st.dataframe(
                correlation_df,
                use_container_width=True
            )

        else:

            st.info(correlation_analysis)