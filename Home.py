import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
    page_title="Home")

#image_path= "C:/Users/umpoz/Documents/REPOS/TESTE_AULA39/"
image = Image.open("log.png")
st.sidebar.image(image, width=120)

st.sidebar.markdown('###### Curry Company')
st.sidebar.markdown('##### Fastest delivery in Town')
st.sidebar.markdown("""___""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as médias de crescimento dos Entregadores e Restaurantes.
    
    ### Como utilizar esse Growth Dashboard?
    
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
        
    - Visão entregador:
        - Acompanhamento dos indicadores semanais de crescimento
        
    - Visao Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
        
    # Ask for Help
         - Time de Data Science no Discord
    """)    

st.sidebar.markdown("""___""")
st.sidebar.markdown(' ### Powered by UMP')










 