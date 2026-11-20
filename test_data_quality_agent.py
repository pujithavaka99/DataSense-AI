import pandas as pd

from agents.data_quality_agent import DataQualityAgent


# Create sample dataset
data = {
    "Name": ["Pujitha", "Rahul", "Pujitha", "Sita"],
    "Age": [23, 24, 23, 25],
    "City": ["Hyderabad", "Chennai", "Hyderabad", "   "],
    "Country": ["India", "India", "India", "India"],
    "Salary": [50000, 0, 60000, 0]
}

df = pd.DataFrame(data)

df.loc[1, "Age"] = None
df.loc[3, "Age"] = None
# Create agent
agent = DataQualityAgent()


# Run analysis
report = agent.run_quality_analysis(df)

quality_score = agent.calculate_quality_score(df)

print("\n========== DATA QUALITY ANALYSIS ==========")

print("\nData Quality Score:", quality_score)


# Display complete report
print("\nData Quality Report:")
print(report)


# Get quality rating
score = report["Data Quality Score"]

rating = agent.get_quality_rating(score)

print("\nQuality Rating:", rating)


# Generate recommendations
recommendations = agent.generate_recommendations(df)

print("\n========== DATA QUALITY RECOMMENDATIONS ==========")

for recommendation in recommendations:
    print("-", recommendation)


# Generate summary
print("\n========== DATA QUALITY SUMMARY ==========")

summary = agent.generate_quality_summary(df)

print(summary)