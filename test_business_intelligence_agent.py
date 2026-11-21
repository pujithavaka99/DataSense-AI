import pandas as pd

from agents.business_intelligence_agent import BusinessIntelligenceAgent


# Create sample business dataset

data = {
    "CustomerID": [101, 102, 103, 104, 105],
    "MonthlyCharges": [50, 75, 100, 60, 90],
    "TotalCharges": [500, 750, 1200, 600, 900],
    "Revenue": [1000, 1500, 2000, 1200, 1800],
    "Profit": [200, 300, 500, 250, 400],
    "Age": [25, 30, 35, 40, 45]
}

df = pd.DataFrame(data)


# Create agent

agent = BusinessIntelligenceAgent()


# Test KPI identification

kpis = agent.identify_business_kpis(df)

# Test KPI summary calculations

kpi_summary = agent.calculate_kpi_summary(
    df,
    kpis
)

print("\n========== KPI SUMMARY ==========\n")

for summary in kpi_summary:

    print(summary)

kpi_insights = agent.generate_kpi_insights(kpi_summary)

print("\n========== KPI INSIGHTS ==========\n")

for insight in kpi_insights:
    print(insight)

performance_insights = agent.identify_kpi_performance(kpi_summary)

print("\n========== KPI PERFORMANCE ==========\n")

for insight in performance_insights:
    print(insight)

variation_insights = agent.analyze_kpi_variation(kpi_summary)

print("\n========== KPI VARIATION ANALYSIS ==========\n")

for insight in variation_insights:
    print(insight)

recommendations = agent.generate_business_recommendations(
    variation_insights
)

print("\n========== BUSINESS RECOMMENDATIONS ==========\n")

for recommendation in recommendations:
    print(recommendation)

profit_margin = agent.calculate_profit_margin(df)

print("\n========== PROFIT MARGIN ANALYSIS ==========\n")

print(profit_margin)

test_df = pd.DataFrame({
    "Age": [25, 30, 35],
    "MonthlyCharges": [50, 75, 100]
})

result = agent.calculate_profit_margin(test_df)

print("\n========== PROFIT MARGIN EDGE CASE ==========\n")

print(result)

# Display results

print("\n========== BUSINESS KPI IDENTIFICATION ==========\n")

for kpi in kpis:

    print(kpi)

zero_revenue_df = pd.DataFrame({
    "Revenue": [0, 0, 0],
    "Profit": [10, 20, 30]
})

result = agent.calculate_profit_margin(zero_revenue_df)

print("\n========== ZERO REVENUE TEST ==========\n")

print(result)

category_df = pd.DataFrame({
    "Region": ["North", "North", "South", "South", "East", "East"],
    "Revenue": [1000, 1500, 2000, 1200, 1800, 2200],
    "Profit": [200, 300, 500, 250, 400, 600]
})

category_analysis = agent.analyze_kpi_by_category(
    category_df,
    "Region",
    "Revenue"
)

category_insights = agent.generate_category_insights(
    category_analysis,
    "Revenue"
)

print("\n========== CATEGORY INSIGHTS ==========\n")

for insight in category_insights:
    print(insight)


category_contribution = agent.calculate_category_contribution(
    category_analysis
)

print("\n========== CATEGORY CONTRIBUTION ==========\n")

print(category_contribution)
print("\n========== KPI BY CATEGORY ==========\n")

print(category_analysis)

contribution_insights = agent.generate_contribution_insights(
    category_contribution,
    "Revenue"
)

print("\n========== CONTRIBUTION INSIGHTS ==========\n")

for insight in contribution_insights:
    print(insight)

empty_category_analysis = pd.DataFrame()

result = agent.calculate_category_contribution(
    empty_category_analysis
)

print("\n========== EMPTY CATEGORY TEST ==========\n")

print(result)