
import plotly.express as px


def plot_churn_by_tenure(tenure_analysis):

    fig = px.bar(
        tenure_analysis,
        x=tenure_analysis.index,
        y="churn_rate",
        title="Customer Churn Rate by Tenure Group",
        labels={
            "tenure_group": "Customer Tenure",
            "churn_rate": "Churn Rate (%)"
        },
        text="churn_rate"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Customer Segment",
        yaxis_range=[0, 60]
    )

    return fig


def plot_churn_by_contract(contract_analysis):

    fig = px.bar(
        contract_analysis,
        x=contract_analysis.index,
        y="churn_rate",
        title="Customer Churn Rate by Contract Type",
        labels={
            "Contract": "Contract Type",
            "churn_rate": "Churn Rate (%)"
        },
        text="churn_rate"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Churn Rate (%)",
        xaxis_title="Contract Type",
        yaxis_range=[0, 50]
    )

    return fig
