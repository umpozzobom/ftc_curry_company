#Import Library

import pandas as pd
import plotly.express as px
from haversine import haversine
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime  #usei esse import para que use o datetime direto e nao o pandar to_datetime
import plotly.graph_objects as go
import numpy as np
st.set_page_config(page_title='Visão Restaurantes', page_icon='', layout = 'wide')

     
#Import dataset

df = pd.read_csv('..dataset/train.csv')
df1 = df.copy()

#------------------------------------------------------------------------------------------------------------#
#                         FUNÇÕES                                                                            #
#------------------------------------------------------------------------------------------------------------#
def avg_std_time_graf(df1):
         df_aux = df1.loc[ :, ['City', 'Time_taken(min)']].groupby(['City']).agg(['mean', 'std'])
         df_aux.columns = ['avg_time', 'std_time']
         df_aux=df_aux.reset_index() 
         fig=go.Figure()
         fig.add_trace(go.Bar(name='Control', x=df_aux['City'],y=df_aux['avg_time'],error_y=dict(type='data', array=df_aux['std_time'])))
         fig.update_layout(barmode='overlay')
         return fig

def avg_std_time_delivery(df1, festival, op):
               df_aux = (df1.loc[ :, ['Time_taken(min)','Festival']]
                         .groupby(['Festival'])
                         .agg({'Time_taken(min)': ['mean', 'std']}))
               df_aux.columns = ['avg_time','std_time']
               df_aux = df_aux.reset_index()
               df_aux = round(df_aux.loc[df_aux['Festival'] == festival,op],2)
               return df_aux

def distancia_localidade(df1):
           cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
           df1['distance'] = df1.loc[: , cols].apply(lambda x:
                                          haversine(
                                              (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                              (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)
           avg_distance = round(df1['distance'].mean(),2)
           return avg_distance
      

def clean_code(df1):
      """ Explicação dos parametos desta função de limpeza do dataframe 

      Tipos de limpezas:

      1. Remoção de espaços
      2. Retirada de NaN
      3. Mudança do tipo de coluna de dados
      4. Remoção dos espaços entre variaveis do texto
      5. Limpeza da coluna de tempo (remoção do texto da variavel numerica)

      input: Dataframe
      output: Dataframe
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
#Import dataset
#---------------------------------

df = pd.read_csv('..dataset/train.csv')

#Limpando dados

df1 = clean_code(df1)

#===========================================================================================#
#     LAYOUT DO STREMEALIT - BARRA LATERAL                                                  #
#===========================================================================================#

st.header('Marketplace - Visão Restaurante')

#image_path = 'log.png'
image=Image.open(log.png)
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

###################################################################################################
#                                   VISÃO RESTAURANTES CÓDIGOS  - MODULARIZADO                    #
#                                                                                                 #
###################################################################################################

#===========================================================================================#
#     LAYOUT DO STREMEALIT - criação das tabs com as informações a serem apresentadas       #
#===========================================================================================#

tab1,tab2,tab3 = st.tabs(['Visão Gerencial', '--','--'])     

with tab1:
    with st.container():
         st.title('Overal Metrics')
         
         col1,col2,col3,col4,col5,col6 = st.columns(6)

         with col1:
           #st.markdown('##### Entregadores únicos')
           unico = df1.loc[: , 'Delivery_person_ID'].nunique()
           col1.metric('Entregadores únicos', unico)
          
         with col2:
             avg_distance = distancia_localidade(df1)
             col2.metric('A distância média das entregas é', avg_distance)
                        

         with col3:
              df_aux = avg_std_time_delivery(df1,'Yes','avg_time')
              col3.metric('Tempo médio', df_aux)
             
         with col4:
           df_aux = avg_std_time_delivery(df1,'Yes','std_time')
           col4.metric('Desvio Padrão de entregas', df_aux)
               
         with col5:
            df_aux = avg_std_time_delivery(df1,'No','avg_time')
            col5.metric('Tempo médio sem Festival', df_aux)
  
         with col6:
           df_aux = avg_std_time_delivery(df1,'No','std_time')
           col6.metric('Desvio Padrão sem Festival', df_aux)

    
    with st.container():
         st.markdown("""---""")
         st.title('Tempo Médio de entrega por cidade')
         fig = avg_std_time_graf(df1)   
         st.plotly_chart(fig)
   
         
    with st.container():
         st.markdown("""---""")
         st.title('Tempo de entrega por Cidade e por densidade')
         col1,col2 = st.columns(2)
        
         with col1:
          st.markdown('##### Média de entrega por cidade')
          cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
          df1['distance'] = df1.loc[: , cols].apply(lambda x:
                                          haversine(
                                              (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                              (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

          avg_distance = df1.loc[: ,['City','distance']].groupby('City').mean().reset_index()

          fig = go.Figure(data=[go.Pie(labels = avg_distance['City'], values = avg_distance['distance'], pull =[0,0,0])])
          st.plotly_chart(fig, use_container_width=True)
       
         with col2:
          st.markdown('##### Tempo de entrega por densidade de trânsito')
          df_aux = (df1.loc[ :, ['City', 'Time_taken(min)','Road_traffic_density']]
                    .groupby(['City','Road_traffic_density'])
                    .agg(['mean', 'std']))

          df_aux.columns = ['avg_time', 'std_time']
          df_aux = df_aux.reset_index()
          fig = px.sunburst(df_aux, path=['City','Road_traffic_density'],values = 'avg_time',
                            color='std_time', color_continuous_scale='RdBu',
                            color_continuous_midpoint=np.average(df_aux['std_time']))
          st.plotly_chart(fig, use_container_width=True)
                        
    with st.container():
         st.markdown("""---""")
         st.title('Tipo de pedido por cidade')
         df_aux = df1.loc[ :, ['City', 'Time_taken(min)','Type_of_order']].groupby(['City','Type_of_order']).agg(['mean', 'std'])
         df_aux.columns=['avg_time', 'std_time']
         df_aux= round(df_aux.reset_index(),2)
         st.dataframe(df_aux)
              











