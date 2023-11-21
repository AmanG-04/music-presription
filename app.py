import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("/home/garvit/Labs/DS Lab/mxmh_survey_results.csv")

# Drop unnecessary columns
df.drop(['Timestamp', 'Permissions'], axis=1, inplace=True)

# Drop rows with missing values in specific columns
df.dropna(subset=['Age', 'Primary streaming service', 'While working', 'Instrumentalist', 'Composer', 'Foreign languages', 'Music effects'], inplace=True)

# Fill missing values in the 'BPM' column with the median
df['BPM'] = df['BPM'].fillna(df['BPM'].median())

# Define upper and lower limits for outlier detection
age_upper_limit = df['Age'].mean() + 3 * df['Age'].std()
BPM_upper_limit = df['BPM'].mean() + 3 * df['BPM'].std()
BPM_lower_limit = df['BPM'].mean() - 3 * df['BPM'].std()
perday_upper_limit = df['Hours per day'].mean() + 3 * df['Hours per day'].std()
perday_lower_limit = df['Hours per day'].mean() - 3 * df['Hours per day'].std()

# Filter out outliers based on the defined limits
new_df = df.loc[(df["Age"] < age_upper_limit) & (df["BPM"] < BPM_upper_limit) & (df["BPM"] > BPM_lower_limit) & (df["Hours per day"] < perday_upper_limit)]

# Display the filtered dataframe
st.write(new_df)

# # Plotting using Streamlit
# st.subheader("Boxplot of Age")
# st.boxplot(new_df['Age'])
# st.subheader("Boxplot of BPM")
# st.boxplot(new_df['BPM'])
# st.subheader("Boxplot of Hours per day")
# st.boxplot(new_df['Hours per day'])

# Heatmap
st.subheader("Correlation Heatmap")
numeric_columns = new_df.select_dtypes(include=[np.number]).columns
correlation_matrix = new_df[numeric_columns].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cbar=True, cmap='Blues', ax=ax)
st.pyplot(fig)

# Countplot
st.subheader("Countplot of Primary streaming service")
fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(x=new_df['Primary streaming service'], ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Pie chart
st.subheader("Effect of music on mental health")
effects = new_df['Music effects'].value_counts()
fig, ax = plt.subplots()
effects.plot(kind='pie', ylabel='', ax=ax)
plt.title("Effect of music on mental health")
st.pyplot(fig)

# Bar plot
st.subheader("Favorite Genre")
y = new_df['Fav genre'].value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
y.plot(kind='bar', ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# Line plots
st.subheader("Mental Health vs. Favorite Genre")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=new_df['Fav genre'], y=new_df['Insomnia'], ci=None, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=new_df['Fav genre'], y=new_df['OCD'], ci=None, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=new_df['Fav genre'], y=new_df['Depression'], ci=None, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=new_df['Fav genre'], y=new_df['Anxiety'], ci=None, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# Bar plot with hue
st.subheader("Favorite Genre vs. Age with Music Effects")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=new_df, x="Fav genre", y="Age", hue="Music effects", errwidth=0, ax=ax)
plt.xticks(rotation=67)
st.pyplot(fig)

# Subplots
st.subheader("Multiple Barplots")
figure, axes = plt.subplots(3, 2, figsize=(18, 10))
sns.barplot(ax=axes[0, 0], x=new_df['Fav genre'], y=new_df['Age'], hue=new_df['Music effects'], palette="rainbow")
sns.barplot(ax=axes[0, 1], x=new_df['Fav genre'], y=new_df['Hours per day'], hue=new_df['Music effects'], palette="rainbow")
sns.barplot(ax=axes[1, 0], x=new_df['Fav genre'], y=new_df['Insomnia'], hue=new_df['Music effects'], palette="rainbow")
sns.barplot(ax=axes[1, 1], x=new_df['Fav genre'], y=new_df['OCD'], hue=new_df['Music effects'], palette="rainbow")
sns.barplot(ax=axes[2, 0], x=new_df['Fav genre'], y=new_df['Depression'], hue=new_df['Music effects'], palette="rainbow")
sns.barplot(ax=axes[2, 1], x=new_df['Fav genre'], y=new_df['Anxiety'], hue=new_df['Music effects'], palette="rainbow")
plt.tight_layout()
st.pyplot(figure)