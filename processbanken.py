import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle

st.title('Processbanken')
st.markdown("""
            Här kan du titta på data från Processbänken 2022.
            - På sidan *Kolla reningsverket* kan du se tidsserier för olika reningsverk och parametrar.
            - På sidan *Jämför* kan jämföra medelvärden för olika parametrar bland de reningsverk som deltog i Processbänken.
            - På sidan *Analysera* kan du undersöka relationen mellan olika parametrar.
            """)
