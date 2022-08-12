import streamlit as st
import pandas as pd
import altair as alt
import pickle

with open('data/dataframe.pickle', 'rb') as f:
    df = pickle.load(f)
df['Datum'] = pd.to_datetime(df['Datum'])

st.title('Kolla reningsverket')
st.markdown('Välj vilket reningsverk och vilka parametrar du vill titta på.')

arv_options = sorted(df[['Stad', 'ARV']].agg(': '.join, axis=1).unique().tolist())
arv = st.selectbox('Välj reningsverk', arv_options)
arv = arv.split(': ')[1]

temp = df[df['ARV'] == arv]
par_options = sorted(temp['Parameter'].unique().tolist())
par = st.multiselect('Välj parametrar', par_options)
temp = temp[temp['Parameter'].isin(par)]

enheter = ''
et = temp.groupby('Parameter').first()
for ix in et.index:
    enheter = enheter + ix + ' (' + et.at[ix, 'Enhet'] + ')  '

tempT = temp[temp['Datum'].notna()]
fig = alt.Chart(tempT).mark_line(point=alt.OverlayMarkDef()).encode(x=alt.X('Datum:T', axis=alt.Axis(format='%Y/%m', title='')), y=alt.Y('Value:Q', axis=alt.Axis(title=enheter)), color='Parameter').properties(width=600, height=400)
#, alt.X('Datum', axis=alt.Axis(title='')), y=alt.Y(p, axis=alt.Axis('')))
st.altair_chart(fig)

tempI = temp[~temp['Datum'].notna()]
tempI = tempI.drop_duplicates()
tempI['cd'] = tempI[['Stad', 'ARV']].agg(': '.join, axis=1)
tempI.set_index('cd', inplace=True)
tempI['Value'] = tempI['Value'].round(decimals=1).astype(str)
st.table(tempI[['Parameter', 'Enhet', 'Value']])
    
