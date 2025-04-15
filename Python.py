import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
df= pd.read_csv(r"C:\Users\hp\Desktop\PYTHON\Project\FINAL_REPORT_7102.csv")


# Display basic info
print("Dataset Overview:")
print(df.head())
print(df.info())
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"\nNumber of duplicate rows: {duplicates}")

df=df.drop_duplicates()

# NumPy-based Summary Statistics
numeric_df = df.select_dtypes(include=[np.number])
print(f"Mean of each column:\n{np.mean(numeric_df, axis=0)}")
print(f"Standard deviation:\n{np.std(numeric_df, axis=0)}")


#OBJECTIVE 1: Analyze State-wise GST Return Filing Trends
i. Introduction
The goal of this analysis is to understand how actively each Indian state participates in GST return filings over the financial year.
This provides a sense of overall tax engagement across regions.

ii. General Description
I’ll group the dataset by State and sum up Total_ReturnFiled to identify the top and bottom performing states in terms of return volume.
This will give us a clear picture of where compliance is highest in absolute numbers.

iii. Functions & Formulas Used
1) groupby() and sum() to aggregate total returns filed.
2) sort_values() to rank states.
3) matplotlib and seaborn for visual representation.

#iv. Analysis Code & Results
# Group by state and calculate total returns filed
returns_before = df.groupby('State')['Gst ( goods and service tax ) payers registered before due date'].sum()
returns_after = df.groupby('State')['Gst ( goods and service tax ) payers registered after due date'].sum()
statewise_returns = returns_before + returns_after

# Sort and preview
statewise_returns = statewise_returns.sort_values(ascending=False)
# Show top 10 states
print(" Top 10 States by Total GST Returns Filed:\n")
print(statewise_returns.head(10))

# Show bottom 5 states
print("\n Bottom 5 States by Total GST Returns Filed:\n")
print(statewise_returns.tail(5))

#v. Visualization
# Plot top 10 states
plt.figure(figsize=(12, 6))
sns.barplot(x=statewise_returns.head(10).values, y=statewise_returns.head(10).index, palette="crest")
plt.title("Top 10 States by Total GST Returns Filed (2017–18)", fontsize=14)
plt.xlabel("Total Returns Filed")
plt.ylabel("State")
plt.tight_layout()
plt.show()


#OBJECTIVE 2: Evaluate Filing Timeliness (Before vs After Due Date)

i. Introduction
Timely tax filing is a strong indicator of regulatory compliance and administrative efficiency.
In this section, we analyze how many GST returns were filed before vs after the due date — state by state — to understand punctuality across India.

ii. General Description
I’ll:
1)Use ReturnFiledBeforeDueDate and ReturnFiledAfterDueDate columns
2)Group by State
3)Calculate percentages and ratios to determine filing behavior
4)Highlight states with the highest and lowest timely filing rates

iii. Functions & Formulas
1)Timely Filing Ratio (TFR):
    TFR = ReturnFiledBeforeDueDate / (ReturnFiledBeforeDueDate + ReturnFiledAfterDueDate)
2)I’ll also compute % Late Filing and % On-Time Filing for comparison.

#iv. Code & Analysis Results
# Group by State and calculate totals for before/after due date
filing_summary = df.groupby('State')[
    ['Gst ( goods and service tax ) payers registered before due date',
     'Gst ( goods and service tax ) payers registered after due date']
].sum()

# Calculate total and percentage
filing_summary['TotalFiled'] = (
    filing_summary['Gst ( goods and service tax ) payers registered before due date'] +
    filing_summary['Gst ( goods and service tax ) payers registered after due date']
)

filing_summary['OnTime%'] = (
    (filing_summary['Gst ( goods and service tax ) payers registered before due date'] /
     filing_summary['TotalFiled']) * 100
)

filing_summary['Late%'] = 100 - filing_summary['OnTime%']

# Sort states by OnTime%
filing_summary_sorted = filing_summary.sort_values(by='OnTime%', ascending=False)

# Display top and bottom 5 states
print("Top 5 States (Timely Filing %):\n", filing_summary_sorted[['OnTime%']].head(5))
print("\nBottom 5 States (Timely Filing %):\n", filing_summary_sorted[['OnTime%']].tail(5))

#v. Visualisation Code
# Bar chart: Top 10 states with highest timely filing %
plt.figure(figsize=(12, 6))
sns.barplot(
    x=filing_summary_sorted['OnTime%'].head(10),
    y=filing_summary_sorted.index[:10],
    palette='crest'
)
plt.xlabel("Timely Filing Percentage (%)")
plt.ylabel("State")
plt.title("Top 10 States by Timely GST Filing (2017–18)")
plt.tight_layout()
plt.show()

# Pie chart: National level filing behavior
total_before = df['Gst ( goods and service tax ) payers registered before due date'].sum()
total_after = df['Gst ( goods and service tax ) payers registered after due date'].sum()

plt.figure(figsize=(6, 6))
plt.pie(
    [total_before, total_after],
    labels=['Filed Before Due Date', 'Filed After Due Date'],
    autopct='%1.1f%%',
    startangle=140,
    colors=['#4CAF50', '#FF6F61']
)
plt.title("National GST Filing Timeliness (2017–18)")
plt.axis('equal')
plt.show()


#OBJECTIVE 3: Does Population Influence GST Filing Behavior?
i. Introduction
This analysis explores whether a state’s total population has an impact on the number of GST (Goods and Services Tax) returns filed.
We want to understand if states with more people are proportionally more compliant or simply generating more returns due to size.

ii. General Description
We use the merged dataset containing GST return filings and demographic information. The analysis focuses on state-wise aggregation of:
1)Total GST returns filed (both before and after due date)
2)Total population
We then calculate a normalized metric: GST Returns filed per 1,000 people to ensure comparability across differently sized states.

iii. Specific Requirements, Functions & Formulas
We used pandas to:
1)Group data by 'State'
2)Sum up GST return filings from:
3)'Gst ( goods and service tax ) payers registered before due date'
4)'Gst ( goods and service tax ) payers registered after due date'

Extract the average of 'TotalPopulation' per state
Calculate returns per 1,000 people using:
Formula:
ReturnsPer1000People = (TotalReturns / TotalPopulation) × 1000
We also computed the Pearson correlation coefficient to determine the strength of linear relationship:
corr(TotalPopulation, TotalReturns)
#iv. Code & Analysis Results
# Group by State
grouped = df.groupby('State').agg({
    'Gst ( goods and service tax ) payers registered before due date': 'sum',
    'Gst ( goods and service tax ) payers registered after due date': 'sum',
    'TotalPopulation': 'mean'  # Assuming total population is same across months
}).reset_index()

# Total Returns Filed
grouped['TotalReturns'] = grouped[
    'Gst ( goods and service tax ) payers registered before due date'
] + grouped[
    'Gst ( goods and service tax ) payers registered after due date'
]

# Calculate returns per 1000 people
grouped['ReturnsPer1000People'] = (grouped['TotalReturns'] / grouped['TotalPopulation']) * 1000

# Sort by highest filing rate
grouped_sorted = grouped.sort_values(by='ReturnsPer1000People', ascending=False)

# View top states
print("Top 5 States by Returns per 1000 People:\n", grouped_sorted[['State', 'ReturnsPer1000People']].head(5))

#v. Visualisation Code
correlation = grouped['TotalPopulation'].corr(grouped['TotalReturns'])
print(f"\n Correlation Coefficient between Population and Returns: {correlation:.2f}")
#Visualization 1: Returns per 1000 People
plt.figure(figsize=(12, 6))
sns.barplot(
    data=grouped_sorted.head(10),
    x='ReturnsPer1000People',
    y='State',
    palette='mako'
)
plt.xlabel("GST Returns per 1000 People")
plt.ylabel("State")
plt.title("Top 10 States by GST Filing Rate per Capita")
plt.tight_layout()
plt.show()

#Visualization 2: Correlation Plot
plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=grouped,
    x='TotalPopulation',
    y='TotalReturns',
    hue='State',
    palette='tab10',
    legend=False
)
plt.xlabel("Total Population")
plt.ylabel("Total GST Returns Filed")
plt.title("Relationship Between Population and GST Filing Volume")
plt.tight_layout()
plt.show()


#Objective 4: Comparative Analysis of GST Return Filings Based on Urban and Rural Population

i. Introduction
The goal of this analysis is to assess whether urban or rural demographics show higher GST return activity.
As India's economy diversifies, it’s important to understand which population segments are driving tax compliance
and how regional development affects filings.

ii. General Description
From the merged dataset, we extract:
1)GST returns (before & after due date)
2)Urban and Rural population figures
We normalize the number of filings against both urban and rural population to derive "filings per 1,000 people" for each population type per state.

iii. Specific Requirements, Functions & Formulas
Steps:
Group dataset by 'State'

Aggregate:

1)Gst ( goods and service tax ) payers registered before due date
2)Gst ( goods and service tax ) payers registered after due date

TotalPopulationUrban

TotalPopulationRural

Compute:

1)TotalReturns = before + after
2)ReturnsPer1000Urban = (TotalReturns / TotalPopulationUrban) × 1000
3)ReturnsPer1000Rural = (TotalReturns / TotalPopulationRural) × 1000

#iv. Analysis Results
# Group and aggregate
grouped = df.groupby("State").agg({
    'Gst ( goods and service tax ) payers registered before due date': 'sum',
    'Gst ( goods and service tax ) payers registered after due date': 'sum',
    'TotalPopulationUrban': 'mean',
    'TotalPopulationRural': 'mean'
}).reset_index()

# Total Returns
grouped['TotalReturns'] = (
    grouped['Gst ( goods and service tax ) payers registered before due date'] +
    grouped['Gst ( goods and service tax ) payers registered after due date']
)

# Filings per 1000 Urban and Rural Residents
grouped['ReturnsPer1000Urban'] = (grouped['TotalReturns'] / grouped['TotalPopulationUrban']) * 1000
grouped['ReturnsPer1000Rural'] = (grouped['TotalReturns'] / grouped['TotalPopulationRural']) * 1000

# View highest urban/rural filing rate
print("\nTop Urban Filing States:\n", grouped[['State', 'ReturnsPer1000Urban']].sort_values(by='ReturnsPer1000Urban', ascending=False).head(5))
print("\nTop Rural Filing States:\n", grouped[['State', 'ReturnsPer1000Rural']].sort_values(by='ReturnsPer1000Rural', ascending=False).head(5))

#v. Visualization:
plt.figure(figsize=(14, 6))
grouped_melted = grouped.melt(id_vars='State', value_vars=['ReturnsPer1000Urban', 'ReturnsPer1000Rural'], 
                              var_name='PopulationType', value_name='ReturnsPer1000')

sns.barplot(data=grouped_melted, x='ReturnsPer1000', y='State', hue='PopulationType', palette='Set2')
plt.title("GST Returns per 1000 People: Urban vs Rural by State")
plt.xlabel("Returns per 1000 People")
plt.ylabel("State")
plt.tight_layout()
plt.show()


#Objective 5: Temporal Trends in GST Return Filings — Are We Getting Better at Compliance?

i. Introduction
This analysis explores how GST return filing patterns have changed over time. By examining filing behavior across months and years,
we can assess whether compliance is improving, staying stagnant, or declining. It also helps us identify seasonal patterns or one-off events that
affect tax behavior.

ii. General Description
From the merged dataset, we extract:

Return counts (before & after due date)

Year and Month of filing
We then aggregate and visualize these over time to detect filing patterns and trends.

iii. Specific Requirements, Functions & Formulas

I’ll:

Group by 'srcYear' and 'srcMonth'

Sum:

'Gst ( goods and service tax ) payers registered before due date'

'Gst ( goods and service tax ) payers registered after due date'

Calculate monthly totals and optionally convert to a datetime index for time-series plotting

#iv. Analysis Results
# Convert to datetime format
df['YearMonth'] = pd.to_datetime(df['srcYear'].astype(str) + '-' + df['srcMonth'].astype(str) + '-01')

# Group and sum
monthly = df.groupby('YearMonth').agg({
    'Gst ( goods and service tax ) payers registered before due date': 'sum',
    'Gst ( goods and service tax ) payers registered after due date': 'sum'
}).reset_index()



# Add total
monthly['TotalReturns'] = (monthly['Gst ( goods and service tax ) payers registered before due date'] + 
                           monthly['Gst ( goods and service tax ) payers registered after due date'])

#v. Visualization:
plt.figure(figsize=(12, 6))
plt.plot(monthly['YearMonth'], monthly['Gst ( goods and service tax ) payers registered before due date'], label='Before Due Date')
plt.plot(monthly['YearMonth'], monthly['Gst ( goods and service tax ) payers registered after due date'], label='After Due Date')
plt.plot(monthly['YearMonth'], monthly['TotalReturns'], label='Total Returns', linestyle='--', color='black')
plt.title("GST Return Filing Trend Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Returns")
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()

