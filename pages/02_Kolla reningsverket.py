import streamlit as st
import pandas as pd
import altair as alt
import pickle

st.title('Kolla reningsverket')

grund_cont = st.container()
bio_cont = st.container()

with grund_cont:
    with open('data/df_grund.pickle', 'rb') as f:
        df = pickle.load(f)
    df['Datum'] = pd.to_datetime(df['Datum'])
    
    st.subheader('Kolla på grunddata: in, ut, krav och volymer')
    st.markdown('Välj vilket reningsverk och vilka parametrar du vill titta på.')
    
    arv_options = sorted(df[['Stad', 'ARV']].agg(': '.join, axis=1).unique().tolist())
    arv = st.selectbox('Välj reningsverk', arv_options)
    arv = arv.split(': ')[1]
    
    temp = df[df['ARV'] == arv]
    par_options = sorted(temp['Parameter'].unique().tolist())
    par = st.multiselect('Välj parametrar', par_options)
    temp = temp[temp['Parameter'].isin(par)]
    
    tempT = temp[temp['Datum'].notna()]
    enheter = ''
    et = tempT.groupby('Parameter').first()
    for ix in et.index:
        enheter = enheter + ix + ' (' + et.at[ix, 'Enhet'] + ')  '
    
    fig = alt.Chart(tempT).mark_line(point=alt.OverlayMarkDef()).encode(x=alt.X('Datum:T', axis=alt.Axis(format='%b %Y', title='')), y=alt.Y('Value:Q', axis=alt.Axis(title=enheter)), color='Parameter').configure_axisX(labelAngle=45).properties(width=600, height=400).interactive()
    st.altair_chart(fig)
    
    tempI = temp[~temp['Datum'].notna()]
    tempI = tempI.drop_duplicates()
    tempI['cd'] = tempI[['Stad', 'ARV']].agg(': '.join, axis=1)
    tempI.set_index('cd', inplace=True)
    tempI['Value'] = tempI['Value'].round(decimals=1).astype(str)
    st.table(tempI[['Parameter', 'Enhet', 'Value']])
    
with bio_cont:
    with open('data/df_bio.pickle', 'rb') as f:
        df_bio = pickle.load(f)
    df_bio['Datum'] = pd.to_datetime(df_bio['Datum'])

    st.subheader('Kolla på data från biologiska processerna')
    st.markdown('Välj vilket reningsverk och vilka parametrar du vill titta på.')
    
    arv_options = sorted(df_bio[['Stad', 'ARV']].agg(': '.join, axis=1).unique().tolist())
    arv = st.selectbox('Välj reningsverk', arv_options)
    arv = arv.split(': ')[1]
    
    temp = df_bio[df_bio['ARV'] == arv]
    temp['Syfte'][~temp['Syfte'].notna()] = ''
    temp['Proc'] = temp[['Process', 'Syfte']].agg(' '.join, axis=1)
    proc = st.selectbox('Välj process', temp['Proc'].unique())
    temp = temp[temp['Proc'] == proc]

    par_options = sorted(temp['Parameter'].unique().tolist())
    par = st.multiselect('Välj parametrar', par_options)
    temp = temp[temp['Parameter'].isin(par)]
    
    tempT = temp[temp['Datum'].notna()]
    enheter = ''
    et = tempT.groupby('Parameter').first()
    tempT['Key'] = ''
    tempT['Key'][tempT['Subprocess'] != ''] = tempT[['Parameter', 'Subprocess']][tempT['Subprocess'] != ''].agg(': '.join, axis=1)
    tempT['Key'][tempT['Subprocess'] == ''] = tempT['Parameter'][tempT['Subprocess'] == '']

    for ix in et.index:
        enheter = enheter + ix + ' (' + et.at[ix, 'Enhet'] + ')  '
    
    fig = alt.Chart(tempT).mark_line(point=alt.OverlayMarkDef()).encode(x=alt.X('Datum:T', axis=alt.Axis(format='%b %Y', title='')), y=alt.Y('Value:Q', axis=alt.Axis(title=enheter)), color='Key').configure_axisX(labelAngle=45).properties(width=600, height=400).interactive()
    st.altair_chart(fig)
    
    tempI = temp[~temp['Datum'].notna()]
    if len(tempI) > 0:
        tempI = tempI.drop_duplicates()
        tempI['cd'] = tempI[['Stad', 'ARV']].agg(': '.join, axis=1)
        tempI.set_index('cd', inplace=True)
        tempI['Value'] = tempI['Value'].round(decimals=1).astype(str)
        st.table(tempI[['Parameter', 'Enhet', 'Value']])
