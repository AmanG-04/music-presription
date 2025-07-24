import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(layout="wide")

with open("designing.css") as source_des:
        st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html=True)
df = pd.read_csv("mxmh_survey_results.csv")

df.drop(['Timestamp', 'Permissions'], axis=1, inplace=True)
#df.rename(columns = {'Video ':'Date'}, inplace=True)
df.dropna(subset=['Age', 'Primary streaming service', 'While working', 'Instrumentalist', 'Composer', 'Foreign languages', 'Music effects'], inplace=True)

df['BPM'] = df['BPM'].fillna(df['BPM'].median())

age_upper_limit = df['Age'].mean() + 3 * df['Age'].std()
BPM_upper_limit = df['BPM'].mean() + 3 * df['BPM'].std()
BPM_lower_limit = df['BPM'].mean() - 3 * df['BPM'].std()
perday_upper_limit = df['Hours per day'].mean() + 3 * df['Hours per day'].std()
perday_lower_limit = df['Hours per day'].mean() - 3 * df['Hours per day'].std()

new_df = df.loc[(df["Age"] < age_upper_limit) & (df["BPM"] < BPM_upper_limit) & (df["BPM"] > BPM_lower_limit) & (df["Hours per day"] < perday_upper_limit)]

st.title("THE MUSIC PRESCRIPTION")

# Create two columns: left for text, right for graphs
left_col, right_col = st.columns([10, 10])  # [width ratio]

with left_col:
    st.markdown("### 🎧 How Different Music Genres Affect Mental Health")

    with st.expander("🕊️ Gospel Music"):
        st.markdown("""
        ✅ Improves **insomnia**, especially in **older adults**.
        """)

    with st.expander("🌙 Lofi Beats"):
        st.markdown("""
        ✅ Calms **OCD, anxiety, and depression**.  
        👥 Mostly preferred by people in their **mid-20s**.
        """)

    with st.expander("🚫 Video Game Music"):
        st.markdown("""
        ❌ Worsens **multiple mental health conditions**.  
        ⚠️ Common among people in their **early 20s** — best to avoid.
        """)

    with st.expander("⚡ Rock"):
        st.markdown("""
        ❌ Linked to increased **insomnia** and **depression**.  
        ⚠️ May do more harm than good for mental health.
        """)

    with st.expander("🎻 Classical"):
        st.markdown("""
        ⚠️ May worsen **OCD, anxiety, and depression**.  
        ✅ Shows promise for **improving insomnia**.
        """)

    with st.expander("🎶 Other Genres (R&B, Jazz, K-pop, etc.)"):
        st.markdown("""
        🟡 Generally have a **neutral or mildly positive** effect.  
        📊 No significant negative associations found.
        """)

    with st.expander("⏰ Listening Duration Matters"):
        st.markdown("""
        ✅ **4–6 hours/day** of Gospel or Lofi → positive mental health outcomes.  
        ❌ Just **2 hours/day** of Video Game or Pop → may worsen conditions.
        """)


with right_col:
    graph_choice = st.selectbox(
        'Select a graph',
        [
            'Primary streaming service',
            'Does music make an impact on your Mental Health?',
            'Favorite Genre',
            'Influence of favorite genre on mental health',
            'Dependency of Genre and various factors on Mental Health'
        ]
    )

    if graph_choice == 'Primary streaming service':
        st.subheader("Primary streaming service")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(x=new_df['Primary streaming service'], palette='Spectral')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    elif graph_choice == 'Does music make an impact on your Mental Health?':
        st.subheader("Does music make an impact on your Mental Health?")
        effects = new_df['Music effects'].value_counts()
        explode = (0, 0.2, 0)
        fig, ax = plt.subplots()
        effects.plot(kind='pie', ylabel='', ax=ax, explode=explode, autopct='%1.1f%%',
                     shadow=True, startangle=90)
        plt.title("Does music make an impact on your Mental Health?")
        st.pyplot(fig)

    elif graph_choice == 'Favorite Genre':
        st.subheader("Favorite Genre")
        y = new_df['Fav genre'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        y.plot(kind='bar', ax=ax, color='g')
        plt.xticks(rotation=60)
        st.pyplot(fig)

    elif graph_choice == 'Influence of favorite genre on mental health':
        st.subheader("Influence of favorite genre on mental health")

        for col in ['Insomnia', 'OCD', 'Depression', 'Anxiety']:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.lineplot(x=new_df['Fav genre'], y=new_df[col], ci=None, ax=ax,
                         marker='*', markerfacecolor='r', markersize=10, linewidth=5)
            plt.xticks(rotation=60)
            st.pyplot(fig)

    elif graph_choice == 'Dependency of Genre and various factors on Mental Health':
        st.subheader("Dependency of Genre and various factors on Mental Health")

        for col in ['Age', 'Hours per day', 'Insomnia', 'OCD', 'Depression', 'Anxiety']:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=new_df['Fav genre'], y=new_df[col], hue=new_df['Music effects'], palette="rainbow")
            plt.tight_layout()
            st.pyplot(fig)
