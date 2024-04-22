#Import Library

import pandas as pd
import plotly.express as px
from haversine import haversine
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime  #usei esse import para que use o datetime direto e nao o pandar to_datetime
st.set_page_config(page_title='Visão Entregadores', page_icon='', layout = 'wide')

     
#Import dataset

df = pd.read_csv('dataset/train.csv')

#print(df.head())

df1 = df.copy()
print(df1)

#------------------------------------------------------------------------------------------------------------#
#                         FUNÇÕES - Modularização                                                            #
#------------------------------------------------------------------------------------------------------------#

def top_delivery(df1, top_asc):
     df2 = (df1.loc[:, ['Delivery_person_ID','City', 'Time_taken(min)']]
       .groupby(['City','Delivery_person_ID'])
       .mean()
       .sort_values(['City','Time_taken(min)'], ascending=top_asc).reset_index())
  
     df_aux01 = df2.loc[df2['City']=='Metropolitian', :].head(3)
     df_aux02 = df2.loc[df2['City']=='Urban',:].head(3)
     df_aux03 = df2.loc[df2['City']=='Semi-Urban',:].head(3)
    
     df3 = pd.concat([df_aux01,df_aux02, df_aux03]).reset_index(drop=True)
     return(df3)

def clean_code(df1):
    """ Explicação da função de limpeza do data_frame
    
    1. Remoção dos NaN
    2. Remoção de espaço entre as váriaveis
    3. Transformação de unidades de medidas - string, objtec, float de acordo com cada tipo de dado
    4. Transformação da informação de datas usando to_datetime
    5. Tirando espaço entre strings
    6. Retirando o min da variavél    
    """
    # 1 - Convertendo Object para inteiro = Delivery_person_Age / / Removendo os NaN
    
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, : ].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    # 1.1 - retirando NAN de Weatherconditions
    
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

#----------------------- ESTRUTURA LÓGICA DO CÓDIGO--------------------------------------------
#--------------------------------
#    Import dataset
#---------------------------------

df = pd.read_csv('dataset/train.csv')

# Clean dateset

df1 = clean_code(df1)

#===========================================================================================#
#     LAYOUT DO STREMEALIT - BARRA LATERAL    - não modularizada                            #
#===========================================================================================#

st.header('Marketplace - Visão Entregador')


image=Image.open('log.png')
st.sidebar.image( image,width=210)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
     value=datetime(2022,4,13),
     min_value=datetime(2022, 2, 11),
     max_value=datetime(2022,4,6),
     format='DD-MM-YYYY')

st.header(date_slider)
st.sidebar.markdown("""___""")

traffic_options = st.sidebar.multiselect(
  'Quais as condições do trânsito?',
  ['Low','Medium','High','Jam'],
  default='Low')

st.sidebar.markdown("""___""")
st.sidebar.markdown('#### Powered by Umpozzobom')

#FILTRO DE DATAS ara o usuario só selecionar o interesse

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)


#FILTRO DE TRÂNSITO para o usuario só selecionar o interesse

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options) #isnin = está em?
df1 = df1.loc[linhas_selecionadas, :]
#st.dataframe(df1)


#===========================================================================================#
# LAYOUT DO STREMEALIT - criação das tabs com as informações a serem apresentadas/MODULAR   #
#===========================================================================================#

tab1,tab2 = st.tabs(['Visão Gerencial', '_'])     

with tab1:
     with st.container():
          st.title('Overall Metrics')          
         
     col1,col2,col3,col4 = st.columns(4, gap='large')        
     with col1:
              #st.subheader('Maior de Idade')  #Ou dá para usr markerdow
              maior = df1.loc[:, 'Delivery_person_Age'].max() 
              col1.metric('Maior de Idade' , maior)            
     with col2:
              #st.subheader('Menor de Idade')
              menor = df1.loc[ :,'Delivery_person_Age'].min()
              col2.metric('Menor de Idade' , menor)
     with col3:
              #st.subheader('Pior condição de veículos')
              min = df1.loc[ :, 'Vehicle_condition'].min()
              col3.metric('Pior condição de veículos' , min)
     with col4:
              #st.subheader('Melhor condição de veículos')
              max = df1.loc[ :, 'Vehicle_condition'].max()     
              col4.metric('Melhor condição de veículos' , max)

     with st.container():
         st.markdown("""----""")
         st.title('Avaliações')
         col1,col2 = st.columns(2, gap='large')
         
      
     with col1:
              st.markdown('##### Avaliação média por entregador')
              media = (df1.loc[ :,['Delivery_person_Ratings','Delivery_person_ID']]
                         .groupby('Delivery_person_ID')
                         .mean().reset_index())
              st.dataframe(media)
     with col2:
              st.markdown('##### Avaliação média por trânsito')
              st.markdown("""----""")
              avg_density = (df1.loc[ :,['Delivery_person_Ratings', 'Road_traffic_density']]
                            .groupby(['Road_traffic_density']).agg({'Delivery_person_Ratings': ['mean', 'std']}))
              #mudança de nome de coluna
              avg_density.columns = ['Delivery_mean','Delivery_std']
              
              #reset index
              
              avg_density = avg_density.reset_index()
              st.dataframe(avg_density)
                    
              st.markdown('##### Avaliação média por Clima') 
              clima= (df1.loc[ :,['Delivery_person_Ratings', 'Weatherconditions']]
                      .groupby(['Weatherconditions']).agg({'Delivery_person_Ratings':['mean', 'std']}))
              
              #mudança de nome de coluna
             
              clima.columns = ['Delivery_mean','Delivery_std']
              
              #reset index
              
              clima = clima.reset_index()
              st.dataframe(clima, use_container_width=True)
                
     with st.container():
         st.markdown("""____""")
         st.title('Velocidade de entregas')
         col1,col2 = st.columns(2)
         
      
     with col1:
             st.markdown('##### Top entregadores mais rápidos')
             df3 = top_delivery(df1, top_asc=True)
             st.dataframe(df3)
             
                      
     with col2:
              st.markdown('##### Top entregadores mais lentos')
              df3 = top_delivery(df1, top_asc=False)
              st.dataframe(df3)
             

          























