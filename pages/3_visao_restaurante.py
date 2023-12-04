#Libraries/ pacotes #streamlit so entende a pagina pages


import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import folium
from haversine import haversine
import numpy as np
from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Restaurantes', layout='wide')

#----------------------------------------------------------#
#   FUNÇÕES                                                #
#----------------------------------------------------------#

def avg_std_time_on_traffic(df1):

    df_aux = ( df1.loc[ : , ['Time_taken(min)', 'City', 'Road_traffic_density']]
                  .groupby(['City', 'Road_traffic_density'])
                  .agg({'Time_taken(min)': ['mean', 'std']}) )

    df_aux.columns = ['avg_time', 'std_time']                                                                                                            
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path = ['City', 'Road_traffic_density'], values='avg_time',
    color='std_time', color_continuous_scale='Rdbu',
    color_continuous_midpoint=np.average(df_aux['std_time'])) 

    return fig


def avg_std_time_graph (df1):
        
    df_aux= df1.loc[ : , ['City', 'Time_taken(min)']].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux=df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar( name = 'Control',x=df_aux['City'],          y=df_aux['avg_time'],error_y=dict(type='data',array=df_aux['std_time'])))
    fig.update_layout(barmode='group')

    return fig


def avg_std_time_delivery(df1, festival, op ):  
    """ 
    esta função calcula o tempo medio e o desvio padrao do tempo de entrega.
    Parâmetros:
        Input:
         - df: dataframe com dados para o calculo
         - op: tipo de operação que precisa ser calculado
              'avg_time': tempo médio
              'std_time': Calcula o desvio padrao do tempo.
        Output:
          -df: Dataframe com 2 colunas e 1 linha          
    """

    df_aux =(df1.loc[ : , ['Time_taken(min)','Festival']]
                .groupby('Festival')
                .agg({ 'Time_taken(min)': ['mean', 'std']}))

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)
    
    return df_aux


def distance(df1, fig):
        if fig == False:
            cols  = ['Restaurant_latitude', 'Restaurant_longitude', 
                    'Delivery_location_latitude', 'Delivery_location_longitude']

            df1['Distance'] = df1.loc[ : , cols].apply( lambda x:
                                   haversine(
                                   ( x['Restaurant_latitude'], x['Restaurant_longitude']),
                                   (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1) 
            avg_distance= np.round(df1['Distance'].mean(), 2)
            return avg_distance
        else: 
            cols  = ['Restaurant_latitude', 'Restaurant_longitude', 
                                'Delivery_location_latitude', 'Delivery_location_longitude']
            df1['Distance'] = df1.loc[ : , cols].apply( lambda x:
                                               haversine(
                                               ( x['Restaurant_latitude'], x['Restaurant_longitude']),
                                               (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1) 
            avg_distance = df1.loc[ : , ['City','Distance']].groupby( 'City').mean().reset_index()
            fig = go.Figure(data= [go.Pie( labels = avg_distance['City'], values = avg_distance['Distance'], pull=[0,0.1,0])])

            return fig
        
           
    
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


#-------------------------------------------------------------------#
#     lAYOYT DO STREAMLIT                                           #
#-------------------------------------------------------------------# 

st.header('Marketplace - Visão Restaurantes')

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
#st.header(date_slider)
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
#st.dataframe(df1.head() )

#Filtro de transito
#isin = filtra as info pelo que o usuario passa

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]


#---------------------------------------------------------#
#    Layout do Stremealit                                 #                                                          #
#---------------------------------------------------------#
#fazer as tab e os container


tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '___','___'])

with tab1:
     with st.container():
        st.title('Overal metrics')           
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        
        with col1:
            entregador_unique = len(df1.loc[ : , 'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos', entregador_unique)

        with col2:
            avg_distance = distance(df1, fig=False)
            col2.metric('Distância média', avg_distance)     
                          
      
        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            col3.metric('Tempo médio de festivais', df_aux)

       
        with col4:
            df_aux = avg_std_time_delivery(df1,'Yes', 'std_time')
            col4.metric('STD de festivais', df_aux)
       
        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')     
            col5.metric('Tempo médio sem festivais', df_aux)
                      
                   
        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time') 
            col6.metric('STD sem festivais', df_aux)

        
with st.container():
    st.markdown("""------------""")
    col1, col2 = st.columns([2, 1])
   

    with col1:
        fig = avg_std_time_graph(df1)           
        st.plotly_chart(fig)    
        
    with col2:
        col2.subheader('Distribuição da distância')
        
        df_aux = ( df1.loc[ : , ['Time_taken(min)', 'City', 'Type_of_order']]
                    .groupby(['City', 'Type_of_order'])
                    .agg({'Time_taken(min)':['mean', 'std']}) )
        df_aux.columns= ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)

with st.container():
    st.markdown("""---""")
    st.title('Distribuição do tempo')
    col1,col2 = st.columns([2,1])
        
    with col1:
        fig = distance (df1, fig= True)            
        st.plotly_chart( fig)        
        
    with col2:
        fig = avg_std_time_on_traffic(df1)    
        st.plotly_chart(fig) 




            
   
        
        

    

    




