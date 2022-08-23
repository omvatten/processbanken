import streamlit as st
import pickle 
import pandas as pd
from PIL import Image

header = st.container()
download = st.container()
imageshow = st.container()

with open('data/dataframe.pickle', 'rb') as f:
    df = pickle.load(f)
arv_options = sorted(df[['Stad', 'ARV']].agg(': '.join, axis=1).unique().tolist())

with header:
    st.title('Processbanken')
    st.markdown("""
                Här kan du titta på data från Processbänken 2022.
                - På sidan *Kolla reningsverket* kan du se tidsserier för olika reningsverk och parametrar.
                - På sidan *Jämför* kan jämföra medelvärden för olika parametrar bland de reningsverk som deltog i Processbänken.
                - På sidan *Analysera* kan du undersöka relationen mellan olika parametrar.
                """)

with download:
    st.subheader('Ladda ner data')
    st.markdown('Om du vill ladda ner rådatan som csv-fil (öppningsbar i Excel) så kan du välja reningsverk och klicka nedan.')

    arv = st.selectbox('Välj reningsverk för datanedladdning', arv_options)
    arvs = arv.split(': ')[1]

    @st.cache
    def convert_df(d):
        return d.to_csv(index=False).encode('latin1')
    st.download_button(label='Ladda ner', data=convert_df(df.loc[df['ARV'] == arvs, ['Stad', 'ARV', 'Parameter', 'Enhet', 'Datum', 'Value']]), file_name='data.csv')
    
with imageshow:
    st.subheader('Visa process')

    arv = st.selectbox('Välj reningsverk att visa', arv_options)
    arvs = arv.split(': ')[1]
    image = Image.open('data/'+arvs+ '.png')
    st.write(arvs)
    st.image(image)