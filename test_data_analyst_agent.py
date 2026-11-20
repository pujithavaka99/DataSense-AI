import pandas as pd

from agents.data_analyst_agent import DataAnalystAgent


# Create sample dataset
data = {
    "Age": [23, 25, 30, 35, 40],
    "Salary": [25000, 30000, 45000, 60000, 80000],
    "Experience": [1, 2, 5, 8, 12],
    "Department": ["HR", "IT", "IT", "Sales", "HR"]
}

df = pd.DataFrame(data)
# Create Data Analyst Agent
agent = DataAnalystAgent()
# Run Outlier Analysis
outlier_result = agent.analyze_outliers(df)
# Run Correlation Analysis
correlation_result = agent.analyze_correlations(df)
# Run Statistical Insights
insights_result = agent.generate_statistical_insights(df)

# Run Numerical Analysis
numerical_result = agent.analyze_numerical_data(df)


# Run Categorical Analysis
categorical_result = agent.analyze_categorical_data(df)


# Display Numerical Results
print("\n========== NUMERICAL ANALYSIS ==========\n")

for column, analysis in numerical_result.items():

    print(f"\nColumn: {column}")

    for metric, value in analysis.items():

        print(f"{metric}: {value}")


# Display Categorical Results
print("\n========== CATEGORICAL ANALYSIS ==========\n")

for column, analysis in categorical_result.items():

    print(f"\nColumn: {column}")

    for metric, value in analysis.items():

        print(f"{metric}: {value}")
print("\n========== OUTLIER ANALYSIS ==========\n")

for column, analysis in outlier_result.items():

    print(f"\nColumn: {column}")

    for metric, value in analysis.items():

        print(f"{metric}: {value}")
print("\n========== CORRELATION ANALYSIS ==========\n")

for relationship, correlation in correlation_result.items():

    print(f"{relationship}: {correlation}")

print("\n========== STATISTICAL INSIGHTS ==========\n")

for insight in insights_result:

    print(f"- {insight}")

# Run Complete Data Analyst Analysis
complete_analysis = agent.run_analysis(df)


print("\n========== COMPLETE DATA ANALYST REPORT ==========\n")

for section, results in complete_analysis.items():

    print(f"\n--- {section} ---")

    if isinstance(results, dict):

        for key, value in results.items():

            print(f"{key}: {value}")

    elif isinstance(results, list):

        for insight in results:

            print(f"- {insight}")

    else:

        print(results)

# Test Empty Dataset
empty_df = pd.DataFrame()

empty_result = agent.run_analysis(empty_df)

print("\n========== EMPTY DATASET TEST ==========\n")

print(empty_result)

# Test Dataset with Missing Values

missing_data = {
    "Age": [23, None, 30, 35, 40],
    "Salary": [25000, 30000, None, 60000, 80000],
    "Department": ["HR", "IT", None, "Sales", "HR"]
}

missing_df = pd.DataFrame(missing_data)

missing_result = agent.run_analysis(missing_df)

print("\n========== MISSING VALUES TEST ==========\n")

for section, results in missing_result.items():

    print(f"\n--- {section} ---")

    print(results)

# Test Columns with All Missing Values

all_missing_data = {
    "Age": [None, None, None],
    "Salary": [None, None, None],
    "Department": [None, None, None]
}

all_missing_df = pd.DataFrame(all_missing_data)

all_missing_result = agent.run_analysis(all_missing_df)

print("\n========== ALL MISSING VALUES TEST ==========\n")

print(all_missing_result)