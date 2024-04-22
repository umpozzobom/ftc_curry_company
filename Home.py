import streamlit as st
from PIL import Image
st.set_page_config(
  page_title="Home")

image_path ='/Users/umpoz/Documents/REPOS/RevisãoExercicíos/'   
image = Image.open(image_path + 'log.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('#Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Curry Company Growth Dashboard')

st.markdown(
  """
  Growth Dashboard foi construído para aocmpanhar as métricas de crescimentos dos Entregadores e Restaurantes.
  ### Como utilizar esse Growth Dashboard;?
   - Visão Empresa:
     - Visão Gerencial: métricas gerais de comportamento.
     - Visão Tática: Indicadores semanais de crescimento
     - Visão Geográfica: Insights de geolocalização.
   - Visao Entregador:
      - Acompanhamento dos indicadores semanais de crescimento.
    - Visao Restaurantes:
      - Indicadores semanais de crescimento dos restaurantes

    ### Ask to help - Ully Pozzobom - Time Data Science
    """)

