import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_pickle('rfm_results_cleaned.pkl')
df_no_out = df.query("Monetary <= 30000")
df_no_out = df_no_out.query("Frequency <= 30")
st.title("RFM VISUALIZATION (Internal only)")


name1, name2 = st.columns(2)
with name1:
    st.markdown("""
Author: Thaweewat Rugsujarit\nEmail: thaweewr@scg.com
""")
with name2:
    st.markdown("""

""")



clist = df['segment2_lv1'].unique()

col1, col2 = st.columns(2)
with col1:
    segments = st.selectbox("Select main segment:" ,clist)
with col2:
    metric = st.selectbox("By Metric:" , ('Recency', 'Monetary', 'Frequency'))
 

st.subheader(f"RFM Segment in {segments} by {metric}")
st.write('Data points:', len(df[df['segment2_lv1'] == segments]))

FMCG_rfm_level_agg = df[df['segment2_lv1'] == segments].groupby('Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']
}).round(1).reset_index()


test = pd.DataFrame(FMCG_rfm_level_agg.to_records())
test.columns = ['index', 'Segment', 'Recency (mean)',
       'Frequency (mean)', 'Monetary (mean)',
       'Count']
test = test[['Segment','Count', 'Recency (mean)',
       'Frequency (mean)', 'Monetary (mean)']]

fig_1 = px.scatter(df_no_out[df_no_out['segment2_lv1'] == segments], x='Recency', y='Monetary', color='Segment')


st.dataframe(test.style.background_gradient(axis=0))


st.subheader(f"RFM Segment in {segments} by {metric}")
fig = px.box(df_no_out[df_no_out['segment2_lv1'] == segments], x="Segment", y=metric, color="Churn_group", points = False)
fig.update_traces(quartilemethod="exclusive") 
st.plotly_chart(fig)

st.subheader(f"{segments} Segment Scatter plot")
st.plotly_chart(fig_1)
