import streamlit as st
import pickle 
import pandas as pd

header = st.container()
with header:
    st.title('Processbanken')
    st.markdown("""
                Här kan du titta på data från Processbänken 2022.
                - På sidan *Kolla reningsverket* kan du se tidsserier för olika reningsverk och parametrar.
                - På sidan *Jämför* kan jämföra medelvärden för olika parametrar bland de reningsverk som deltog i Processbänken.
                - På sidan *Analysera* kan du undersöka relationen mellan olika parametrar.
                """)

download = st.container()
with download:
    st.subheader('Ladda ner data')
    st.markdown('Om du vill ladda ner rådatan som csv-fil (öppningsbar i Excel) så kan du välja reningsverk och klicka nedan.')

    with open('data/dataframe.pickle', 'rb') as f:
        df = pickle.load(f)
    arv_options = sorted(df[['Stad', 'ARV']].agg(': '.join, axis=1).unique().tolist())
    arv = st.selectbox('Välj reningsverk', arv_options)
    arv = arv.split(': ')[1]

    @st.cache
    def convert_df(d):
        return d.to_csv(index=False).encode('latin1')
    st.download_button(label='Ladda ner', data=convert_df(df.loc[df['ARV'] == arv, ['Stad', 'ARV', 'Parameter', 'Enhet', 'Datum', 'Value']]), file_name='data.csv')