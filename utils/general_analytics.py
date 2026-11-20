import pandas as pd
import plotly.express as px

def detect_id_columns(df):

    id_columns = []

    for column in df.columns:

        column_lower = column.lower()

        # Detect common ID column names
        if (
            column_lower == "id"
            or column_lower.endswith("_id")
            or column_lower.endswith("id")
        ):
            id_columns.append(column)

        # Detect columns where almost every value is unique
        elif (
            df[column].nunique() / len(df) > 0.95
            and df[column].dtype == "object"
        ):
            id_columns.append(column)

    return id_columns

def analyze_general_dataset(df):

    analysis = {}

    # -----------------------------------------
    # 1. DETECT ID COLUMNS
    # -----------------------------------------

    id_columns = detect_id_columns(df)

    analysis["id_columns"] = id_columns

    # -----------------------------------------
    # 2. IDENTIFY NUMERICAL COLUMNS
    # -----------------------------------------

    numerical_columns = [
        column
        for column in df.select_dtypes(include=["number"]).columns
        if column not in id_columns
    ]

    # -----------------------------------------
    # 3. IDENTIFY CATEGORICAL COLUMNS
    # -----------------------------------------

    categorical_columns = [
        column
        for column in df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns
        if column not in id_columns
    ]

    analysis["numerical_columns"] = numerical_columns

    analysis["categorical_columns"] = categorical_columns

    # -----------------------------------------
    # 4. NUMERICAL ANALYSIS
    # -----------------------------------------

    if numerical_columns:

        analysis["numerical_summary"] = df[
            numerical_columns
        ].describe().round(2)

    else:

        analysis["numerical_summary"] = None

    # -----------------------------------------
    # 5. CATEGORICAL ANALYSIS
    # -----------------------------------------

    categorical_summary = {}

    for column in categorical_columns:

        value_counts = df[column].value_counts(
            dropna=False
        )

        mode_values = df[column].mode(
            dropna=True
        )

        categorical_summary[column] = {

            "unique_values": int(
                df[column].nunique()
            ),

            "most_common_value": (
                mode_values.iloc[0]
                if not mode_values.empty
                else None
            ),

            "most_common_count": (
                int(value_counts.iloc[0])
                if not value_counts.empty
                else 0
            )
        }

    analysis["categorical_summary"] = categorical_summary

    # -----------------------------------------
    # 6. RETURN COMPLETE ANALYSIS
    # -----------------------------------------

    return analysis

import plotly.express as px

def recommend_chart_type(df, column):

    # Numeric columns
    if pd.api.types.is_numeric_dtype(df[column]):

        return (
            "📊 Histogram",
            "This column contains numerical data. "
            "A histogram helps understand its distribution."
        )

    # Categorical columns
    unique_count = df[column].nunique()
    total_count = len(df)

    unique_ratio = (
        unique_count / total_count
        if total_count > 0
        else 0
    )

    # High-cardinality categorical
    if unique_ratio > 0.50:

        return (
            "📊 Top 15 Bar Chart",
            "This column contains many unique values. "
            "Displaying the top 15 values makes the chart easier to interpret."
        )

    # Normal categorical
    return (
        "📊 Bar Chart",
        "This column contains categorical data. "
        "A bar chart helps compare the frequency of different categories."
    )


def create_general_visualization(df, column):

    import plotly.express as px

    # ------------------------------------------
    # Remove missing values for visualization
    # ------------------------------------------

    data = df[column].dropna()

    if data.empty:

        fig = px.bar(
            x=["No Data"],
            y=[0],
            title=f"No data available for {column}"
        )

        return fig

    # ------------------------------------------
    # NUMERICAL COLUMN
    # ------------------------------------------

    if pd.api.types.is_numeric_dtype(df[column]):

        fig = px.histogram(
            df,
            x=column,
            title=f"Distribution of {column}",
            nbins=30
        )

        fig.update_layout(
            xaxis_title=column,
            yaxis_title="Frequency",
            template="plotly_dark"
        )

        return fig

    # ------------------------------------------
    # DATETIME COLUMN
    # ------------------------------------------

    if pd.api.types.is_datetime64_any_dtype(df[column]):

        date_counts = (
            df[column]
            .dropna()
            .value_counts()
            .sort_index()
        )

        fig = px.line(
            x=date_counts.index,
            y=date_counts.values,
            title=f"Trend of {column}"
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Count",
            template="plotly_dark"
        )

        return fig

    # ------------------------------------------
    # CATEGORICAL COLUMN
    # ------------------------------------------

    value_counts = data.astype(str).value_counts()

    unique_count = data.nunique()

    total_count = len(data)

    unique_ratio = unique_count / total_count if total_count else 0

    # ------------------------------------------
    # HIGH CARDINALITY
    # ------------------------------------------

    if unique_ratio > 0.50:

        top_values = value_counts.head(15)

        fig = px.bar(
            x=top_values.index,
            y=top_values.values,
            title=f"Top 15 Values in {column}",
            labels={
                "x": column,
                "y": "Count"
            }
        )

        fig.update_layout(
            xaxis_title=column,
            yaxis_title="Count",
            template="plotly_dark",
            xaxis_tickangle=-45
        )

        return fig

    # ------------------------------------------
    # NORMAL CATEGORICAL COLUMN
    # ------------------------------------------

    top_values = value_counts.head(15)

    fig = px.bar(
        x=top_values.index,
        y=top_values.values,
        title=f"Distribution of {column}",
        labels={
            "x": column,
            "y": "Count"
        }
    )

    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count",
        template="plotly_dark",
        xaxis_tickangle=-45
    )

    return fig

def create_correlation_heatmap(df, numerical_columns):

    import plotly.express as px

    # Check if numerical columns exist
    if len(numerical_columns) < 2:

        return None

    # Calculate correlation
    correlation_matrix = df[numerical_columns].corr()

    # Create heatmap
    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Numerical Feature Correlation Heatmap"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600
    )

    return fig
def explain_correlations(df, numerical_columns):

    if len(numerical_columns) < 2:
        return ["Not enough numerical columns to analyze correlations."]

    correlation_matrix = df[numerical_columns].corr()

    correlation_pairs = []

    # Find unique correlation pairs
    for i in range(len(numerical_columns)):
        for j in range(i + 1, len(numerical_columns)):

            col1 = numerical_columns[i]
            col2 = numerical_columns[j]

            correlation = correlation_matrix.loc[col1, col2]

            correlation_pairs.append({
                "column_1": col1,
                "column_2": col2,
                "correlation": correlation
            })

    # Sort by absolute correlation strength
    correlation_pairs.sort(
        key=lambda x: abs(x["correlation"]),
        reverse=True
    )

    # Get top 3 correlations
    top_correlations = correlation_pairs[:3]

    insights = []

    for pair in top_correlations:

        col1 = pair["column_1"]
        col2 = pair["column_2"]
        correlation = pair["correlation"]

        if correlation >= 0.7:
            strength = "Strong positive"
            explanation = (
                "Both variables tend to increase together."
            )

        elif correlation <= -0.7:
            strength = "Strong negative"
            explanation = (
                "One variable tends to increase as the other decreases."
            )

        elif correlation >= 0.4:
            strength = "Moderate positive"
            explanation = (
                "The variables show a moderate positive relationship."
            )

        elif correlation <= -0.4:
            strength = "Moderate negative"
            explanation = (
                "The variables show a moderate negative relationship."
            )

        else:
            strength = "Weak"
            explanation = (
                "The relationship between these variables is weak."
            )

        insights.append(
            f"**{strength} correlation:** "
            f"`{col1}` and `{col2}` "
            f"({correlation:.2f}). {explanation}"
        )

    return insights