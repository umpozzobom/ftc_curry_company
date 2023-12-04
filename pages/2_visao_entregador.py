#Libraries/ pacotes


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Entregadores', layout='wide')



#--------------------------------------------------------------------
# FUNÇÕES                                                           #
#---------------------------------------------------------------------


def top_delivers(df1, top_asc): 
    df2 = (df1.loc[: , ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby(['City','Delivery_person_ID'])
              .mean().sort_values(['Time_taken(min)', 'City'], ascending = False) 
              .reset_index() )

    df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux2 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop = True)
            
    return df3     
       

def clean_code (df1):
    
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()
    df1['Delivery_person_Age'] = df1["Delivery_person_Age"].astype(int)

    # 1.1 - retirando NAN

    linhas_selecionadas = df1['Weatherconditions'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    # 1.1 - retirando NAN

    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()


    # 2- Convertendo order_date usaod pd.to_datetime

    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')


    # 3 - convertendo Delivery_person_Ratings  - objetc par float

    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 4 - Convertendo deliveris_ Objetc = int

    linhas_selecionadas_mult = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas_mult, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #Retirando os espaços entre strings usando a função str.strip()

    df1.loc[:, 'Delivery_person_ID'] = df1.loc[: , 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'ID'] = df1.loc[: , 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[: , 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[: , 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[: , 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[: , 'City'].str.strip()

    #retirando o min

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split( '(min)' ) [1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    return df1


#Import dataset

df1 = pd.read_csv('train.csv')

#Comando para limpar dados

df1 = clean_code(df1)


############################################################################
#  lAYOYT DO STREAMLIT
#
#############################################################################

st.header('Marketplace - Visão entregadores')

#image_path = 'log.png'
image = Image.open('log.png')
st.sidebar.image(image, width=120)


st.sidebar.markdown('### Curry Company')
st.sidebar.markdown('## Fastest delivery in Town')
st.sidebar.markdown("""___""")

st.sidebar.markdown(' ## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022,4,13),
    min_value=pd.datetime(2022,2,11),
    max_value=pd.datetime(2022,4,6),
    format='DD-MM-YYYY')
st.header(date_slider)
st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low','Medium','High','Jam'],
    default = ['Low','Medium','High', 'Jam'])

st.sidebar.markdown("""___""")
st.sidebar.markdown(' ### Powered by UMP')

#Filtro de data

linhas_selecionadas = df1['Order_Date']< date_slider
df1 = df1.loc[linhas_selecionadas, : ]
st.dataframe(df1.head() )

#Filtro de transito
#isin = filtra as info pelo que o usuario passa

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


############################################################################
# lAYOYT DO STREAMLIT
#
#############################################################################

tab1, tab2,tab3 = st.tabs(['Visão Gerencial', '--', '--'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
       
        col1,col2,col3,col4 = st.columns (4, gap = 'large')
        
        def calcule_big_number(df1):
            with col1:
                #st.subheader('Maior de idade')
                maior_idade = df1.loc[ : , 'Delivery_person_Age'].max()
                col1.metric('Maior de idade', maior_idade)

            with col2:
                #st.subheader('Menor de idade')
                menor_idade = df1.loc[ : ,'Delivery_person_Age'].min() 
                col2.metric('Menor de idade',menor_idade)

            with col3:
                #st.subheader('Melhor condição de veículos')
                melhor = df1.loc[ : , 'Vehicle_condition'].max() 
                col3.metric('Melhor condição de veículos', melhor)            

            with col4:
                #st.subheader("Pior condição de veículos")
                pior = df1.loc[ : , 'Vehicle_condition'].min()
                col4.metric('Pior condição de veículos', pior)  
                
            return df1
         
            
with st.container():
    st.markdown("""___""")
    st.title('Avaliações')
        
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Avaliação média por Entregador")
        df1_aux = ( df1.loc[ : , ['Delivery_person_ID', 'Delivery_person_Ratings']]
                       .groupby('Delivery_person_ID')
                       .mean()
                       .reset_index() )
        st.dataframe(df1_aux)
   
    with col2:
        st.subheader("Avaliação média por trânsito")
        df1_aux = (df1.loc[ : , ['Delivery_person_Ratings', 'Road_traffic_density']]
                     .groupby('Road_traffic_density')
                     .agg(['mean', 'std']) )
                
        df1_aux.columns=["delivery_mean", 'delivery_std']
        df1_aux = df1_aux.reset_index()
        st.dataframe(df1_aux)
            
            
        st.subheader("Avaliação média por clima")
        df1_aux = df1.loc[ : , ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg(['mean', 'std'])

        df1_aux.columns=["delivery_mean", 'delivery_std']

        df1_aux = df1_aux.reset_index()
        st.dataframe(df1_aux)
            
            
with st.container():
        st.markdown("""___""")
        st.title('Velocidade de entrega')
        
col1,col2 = st.columns(2)

with col1:
        st.subheader("Top entregadores mais rápido")
        df3 = top_delivers(df1, top_asc=True)
        st.dataframe(df3)
                                     
with col2:
        st.subheader("Top entregadores mais lentos")
        df3 = top_delivers(df1, top_asc=False)
        st.dataframe(df3)
                   
             
        
           
        
        
        
            