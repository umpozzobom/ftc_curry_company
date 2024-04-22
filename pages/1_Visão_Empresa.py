#Import Library


import pandas as pd
import plotly.express as px
from haversine import haversine
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime

st.set_page_config(page_title='Visão Empresa', page_icon=':)', layout = 'wide')


#Import dataset

df = pd.read_csv('dataset/train.csv')
df1 = df.copy()
print(df1)

#------------------------------------------------------------------------------------------------------------#
#                         FUNÇÕES                                                                            #
#------------------------------------------------------------------------------------------------------------#

def contry_maps(df1):
    df_aux = (df1.loc[ :,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']]
          .groupby(['City','Road_traffic_density'])
          .median()
          .reset_index() )
    maps = folium.Map()
    
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                    location_info['Delivery_location_longitude']],
                   popup=location_info[['City', 'Road_traffic_density']]).add_to(maps)
    folium_static(maps, width=1024 , height=600)
        

def order_share_week(df1):
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby(['week_of_year']).nunique().reset_index()
    df_aux03 = pd.merge(df_aux, df_aux2, how='inner') #daqui que irei fazer a divisão
    df_aux03['qtd_entregas_week'] = df_aux03['ID']/df_aux03['Delivery_person_ID']
    fig = px.line(df_aux03, x ='week_of_year', y ='qtd_entregas_week' )
    return fig

def order_week(df1):
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[ :, ['week_of_year', 'ID']].groupby(['week_of_year']).count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return (fig)

def traffic_order_city(df1):
    df_aux = df1.loc[: ,['ID', 'City','Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color = 'City', size_max = 30)
    return fig
        
def traffic_order_density (df1):
    df_aux = df1.loc[: , ['Road_traffic_density', 'ID']].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID']/df_aux['ID'].sum()
    fig = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density')
    return fig

def order_metric(df1):
    #Order metric
    columns = ['ID', 'Order_Date']
    #Seleção de linhas
    df_aux = df1.loc[ :, columns].groupby(['Order_Date']).count().reset_index()
    #Desenhar gráficos de linha
    fig = px.bar(df_aux, x='Order_Date', y='ID')
    return fig
  
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

df = pd.read_csv('dataset/train.csv')

#Limpando dados

df1 = clean_code(df1)

###################################################################################################
#                                   VISÃO EMPRESA CÓDIGOS                                         #
#                                                                                                 #
###################################################################################################
#===========================================================================================#
#     LAYOUT DO STREMEALIT - BARRA LATERAL                                                  #
#===========================================================================================#

st.header('Marketplace - Visão Cliente')

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

#st.header(date_slider)
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
#     LAYOUT DO STREMEALIT - criação das tabs com as informações a serem apresentadas       #
#===========================================================================================#
tab1, tab2,tab3 = st.tabs (['Visão Gerencial' , 'Visão Tática', 'Visão Geográfica'])     

with tab1:
  with st.container():
       fig = order_metric(df1)
       st.markdown('#### Order by day')
       st.plotly_chart(fig, use_container_width=True)  
        
  with st.container():
    #st.markdown('## Order by traffic')
    col1,col2 = st.columns(2)
    
    with col1:
         fig = traffic_order_density(df1)
         st.header("Traffic Order Density")
         st.plotly_chart(fig, use_container_width=True)
       
    with col2:
        fig = traffic_order_city(df1)
        st.header("Traffic Order City")
        st.plotly_chart(fig, use_container_width=True)     
          
with tab2:
  with st.container():
       fig = order_week(df1)
       st.markdown('###### Order by Week')
       st.plotly_chart(fig, use_container_width=True)

  with st.container():  
       fig = order_share_week(df1)
       st.markdown('###### Order share by Week')
       st.plotly_chart(fig, use_container_width=True)
  
     
with tab3:
     st.header("Country Maps")
     contry_maps(df1)
    
    
  
    




