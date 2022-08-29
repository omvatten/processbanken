import streamlit as st
import pandas as pd
import altair as alt
import pickle

st.title('Analysera')
grund_cont = st.container()
avg_cont = st.container()

with grund_cont:
    with open('data/df_grund.pickle', 'rb') as f:
        df = pickle.load(f)
    df['Datum'] = pd.to_datetime(df['Datum'])
    st.subheader('Kolla på grunddata: in, ut, krav och volymer')
    st.markdown('Undersök samband mellan olika parametrar.')
    
    tslist = df.loc[df['Datum'].notna(), 'Parameter'].unique().tolist()
    flist = df.loc[~df['Datum'].notna(), 'Parameter'].unique().tolist()
    parametrar = sorted(tslist)+sorted(flist)
    par1 = st.selectbox('Välj parameter 1', parametrar, index=1)
    par2 = st.selectbox('Välj parameter 2', parametrar, index=3)
    
    if par1 in tslist and par2 in tslist:
        temp = df[df['Parameter'].isin([par1, par2])]
        temp['cd'] = temp['Kod'] + temp['Datum'].astype(str)
        temp = temp.pivot(index='cd', columns='Parameter', values=['Value', 'ARV', 'Enhet'])
        mask = temp.notna().all(axis=1)
        temp = temp.loc[mask[mask].index]
        temp1 = temp['Value']
        temp1['ARV'] = temp['ARV'][par1].copy()
        par1_enhet = temp['Enhet'][par1].iloc[0]
        par2_enhet = temp['Enhet'][par2].iloc[0]
        del temp
        fig = alt.Chart(temp1).mark_circle().encode(x=alt.X(par1, axis=alt.Axis(title=par1+' ('+par1_enhet+')')), y=alt.Y(par2, axis=alt.Axis(title=par2+' ('+par2_enhet+')')), color='ARV').properties(width=600, height=400)
        st.altair_chart(fig)
    
    elif (par1 in tslist or par2 in tslist) and (par1 in flist or par2 in flist):
        if par1 in tslist:
            tpar = par1
            fpar = par2
        else:
            tpar = par2
            fpar = par1
    
        tempT = df[df['Parameter'] == tpar]
        tempT = tempT[tempT['Value'].notna()]
        tpar_enhet = tempT['Enhet'].iloc[0]
        tempTavg = tempT.groupby('ARV').mean()
        tempTstd = tempT.groupby('ARV').std()
    
        tempF = df[df['Parameter'] == fpar]
        fpar_enhet = tempF['Enhet'].iloc[0]
        tempF = tempF.groupby('ARV').mean()
        tempF[fpar] = tempF['Value']
        tempF[tpar] = tempTavg['Value']
        tempF['std'] = tempTstd['Value']
        tempF['ymin'] = tempF[tpar]-tempF['std']
        tempF['ymax'] = tempF[tpar]+tempF['std']
        tempF = tempF.reset_index()
        del tempT
        chart = alt.Chart(tempF)
        points = chart.mark_circle().encode(x=alt.X(fpar, axis=alt.Axis(title=fpar+' ('+fpar_enhet+')')), y=alt.Y(tpar, axis=alt.Axis(title=tpar+' ('+tpar_enhet+')')), color='ARV').properties(width=800, height=400)
        yerr = chart.mark_errorbar().encode(x=fpar, y='ymin', y2='ymax', color='ARV')
        fig = points + yerr
        st.altair_chart(fig)
    
    elif par1 in flist and par2 in flist:
        temp = df.loc[df['Parameter'].isin([par1, par2]), ['ARV', 'Parameter', 'Enhet', 'Value']]
        temp = temp.drop_duplicates()
        temp = temp.pivot(index='ARV', columns='Parameter', values=['Value', 'ARV', 'Enhet'])
        mask = temp.notna().all(axis=1)
        temp = temp.loc[mask[mask].index]
        temp1 = temp['Value']
        temp1['ARV'] = temp['ARV'][par1]
        par1_enhet = temp['Enhet'][par1].iloc[0]
        par2_enhet = temp['Enhet'][par2].iloc[0]
        del temp
        fig = alt.Chart(temp1).mark_circle().encode(x=alt.X(par1, axis=alt.Axis(title=par1+' ('+par1_enhet+')')), y=alt.Y(par2, axis=alt.Axis(title=par2+' ('+par2_enhet+')')), color='ARV').properties(width=600, height=400)
        st.altair_chart(fig)
    
with avg_cont:
    with open('data/yearly_averages.pickle', 'rb') as f:
        df = pickle.load(f)
    st.subheader('Kolla på beräknade årsmedelvärden')
    st.markdown('Undersök samband mellan olika parametrar.')
    
    parametrar = sorted(df['Parameter'].unique().tolist())
    par1 = st.selectbox('Välj parameter 1', parametrar, index=5, key='avg1')
    par2 = st.selectbox('Välj parameter 2', parametrar, index=6, key='avg2')

    temp = df[df['Parameter'].isin([par1, par2])]
    temp['cd'] = df[['ARV', 'Process']].agg(': '.join, axis=1)
    temp = temp.pivot(index='cd', columns='Parameter', values=['Value', 'Enhet'])
    mask = temp.notna().all(axis=1)
    temp = temp.loc[mask[mask].index]
    temp1 = temp['Value']
    temp1['cd'] = temp1.index
    par1_enhet = temp['Enhet'][par1].iloc[0]
    par2_enhet = temp['Enhet'][par2].iloc[0]
    del temp
    fig = alt.Chart(temp1).mark_circle(size=150).encode(x=alt.X(par1, axis=alt.Axis(title=par1+' ('+par1_enhet+')')), y=alt.Y(par2, axis=alt.Axis(title=par2+' ('+par2_enhet+')')), tooltip='cd').properties(width=600, height=400)
    st.altair_chart(fig)
