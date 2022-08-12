import streamlit as st
import pandas as pd
import altair as alt
import pickle

with open('data/dataframe.pickle', 'rb') as f:
    df = pickle.load(f)
df['Datum'] = pd.to_datetime(df['Datum'])

st.title('Jämför reningsverken')
st.markdown('Välj vilken parameter du vill titta på.')

parametrar = ['Reaktorvolymer', 'Flöde', 'BOD7', 'TP', 'TN', 'NH4', 'COD', 'TOC']
par = st.selectbox('Välj parameter', parametrar)


arv_options = sorted(df[['Stad', 'ARV']].agg(': '.join, axis=1).unique().tolist())
arv = st.multiselect('Välj reningsverk', arv_options, default=arv_options)
arv = [c.split(': ')[1] for c in arv]

if par == 'Reaktorvolymer':
    mt = df[df['ARV'].isin(arv)]
    mt = mt.loc[mt['Parameter'].isin(['Vol_FS', 'Vol_ES', 'Vol_AS', 'Vol_BF']), ['ARV', 'Parameter', 'Value']]
    mt = mt.drop_duplicates()
    mt = mt.pivot(index='ARV', columns='Parameter', values='Value')
    mt = mt.reset_index()
    #https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    base_chart = alt.Chart(mt).mark_bar().encode(x=alt.X('ARV', axis=alt.Axis(title=''))).properties(width=300, height=200)
    fs_c = base_chart.encode(y=alt.Y('Vol_FS', axis=alt.Axis(title='Försed. (m\u00B3)')), tooltip='Vol_FS')
    es_c = base_chart.encode(y=alt.Y('Vol_ES', axis=alt.Axis(title='Eftersed. (m\u00B3)')), tooltip='Vol_ES')
    as_c = base_chart.encode(y=alt.Y('Vol_AS', axis=alt.Axis(title='Aktivslam (m\u00B3)')), tooltip='Vol_AS')
    bf_c = base_chart.encode(y=alt.Y('Vol_BF', axis=alt.Axis(title='Biofilm (m\u00B3)')), tooltip='Vol_BF')
    fig = (fs_c | es_c) & (as_c | bf_c)
    st.altair_chart(fig)

elif par == 'Flöde':
    mt = df[(df['ARV'].isin(arv))&(df['Parameter'] == 'Q_in')]
    mt['Flöde (m\u00B3/d)'] = mt['Value']
    fig = alt.Chart(mt).mark_boxplot().encode(x=alt.X('ARV', axis=alt.Axis(title='')), y='Flöde (m\u00B3/d)').properties(width=600, height=400)
    st.altair_chart(fig)

else:
    mt = df[(df['ARV'].isin(arv))&(df['Parameter'].isin([par+'_in', par+'_ut']))]
    mtIN = mt[mt['Parameter'] == par+'_in']
    yin = par+' in ('+mtIN['Enhet'].iloc[0]+')'
    mtIN[yin] = mtIN['Value']
    mtUT = mt[mt['Parameter'] == par+'_ut']
    yut = par+' ut ('+mtUT['Enhet'].iloc[0]+')'
    mtUT[yut] = mtUT['Value']

    chart1 = alt.Chart(mtIN).mark_boxplot().encode(x=alt.X('ARV', axis=alt.Axis(title='')), y=yin).properties(width=400, height=400)
    chart2 = alt.Chart(mtUT).mark_boxplot().encode(x=alt.X('ARV', axis=alt.Axis(title='')), y=yut).properties(width=400, height=400)
    fig = chart1 | chart2
    st.altair_chart(fig)
