import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import glob
import os
from urllib.request import urlopen
import json
from streamlit_folium import folium_static
from st_aggrid import AgGrid
import geopandas as gpd
import folium
from functools import reduce
from folium.plugins import FloatImage
import urllib
import unidecode
import requests



LogoComision="data:image/png;base64,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"
LogoComision2="https://www.postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png"

st.set_page_config(
    page_title="Indice de calidad CRC", page_icon=LogoComision,layout="wide",initial_sidebar_state="expanded")
    
Estilo_css="""<style type="text/css">
    @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap'); 

    html, body, [class*="css"] ,[class*="st-ae"]{
        font-family: 'Poppins', serif; 
    }  
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 300px;background-color:#2A3144;color=white;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 300px;
        top:100px;
        background-color:#2A3144;
        color=white;
        margin-left: -300px;}
    h1{ background: #EEF3F4;
        text-align: center;
        padding: 15px;
        font-family: Poppins;
        font-size:1.60rem;
        color: black;
        position:fixed;
        width:100%;
        z-index:9999999;
        top:80px;
        left:0;
    }
    h2{
        background: #fffdf7;
        text-align: center;
        padding: 10px;
        color: #FE9D82;
        font-weight: bold;
    }    
    h6{
        background: #fffdf7;
        color: #7a44f2;
        font-weight: bold;
    }        
    .barra-superior{top: 0;
        position: fixed;
        background-color: #FE9D82;
        width: 100%;
        color:white;
        z-index: 999;
        height: 80px;
        left: 0px;
        text-align: center;
        padding: 0px;
        font-size: 36px;
        font-weight: 700;
    }
    .css-1wrcr25{
        margin-top:135px;
    }
    .e16nr0p31 {display:none}
    .css-y3whyl, .css-xqnn38 {background-color:#ccc}
    .e8zbici0 {display:none}
    .e8zbici2 {display:none}
    .e19lei0e1 {display:none}
    .css-1uvyptr:hover,.css-1uvyptr {background: #ccc}
    .e1tzin5v2 {
        display:flex;
        align-items:center;
    }
    .e1fqkh3o2{
        padding-top:2.5rem;   
    }
    .css-52bwht{
        gap:0.01rem;
    }
    .block-container {
        padding-top:0;
        } 
    .main > div {
        padding-left:30px;
        padding-right:30px;
    }            
    .titulo {
      background: #fffdf7;
      display: flex;
      color: #7a44f2;
      font-size:25px;
      padding:10px;
      text-align:center;
    }
    .titulo:before,
    .titulo:after {
      content: '';
      margin: auto 1em;
      border-bottom: solid 3px;
      flex: 1;
    }   
    .stButton{
        text-align:center;
    }
    .edgvbvh9:hover {
      color:rgb(255,255,255);
      border-color:rgb(255,75,75);
    }
    .edgvbvh9 {
      font-weight: 600;
      background-color: rgb(215,235,252);
      border: 0px solid rgba(0, 0, 0, 1); 
      color:black;
      padding: 0.6rem 0.6rem;
      font-size: 16px;
    }
    .imagen-flotar{float:left;}
    @media (max-width:1230px){
        .barra-superior{height:160px;} 
        .main, .e1fqkh3o9 > div{margin-top:215px;}
        .imagen-flotar{float:none}
        h1{top:160px;}}       
    .IconoTitulo img {
        margin-right:10px;
    }
    .IconoTitulo{
        text-align:center;
    }
    .IconoTitulo h4, .IconoTitulo img {
        display:inline-block;
        vertical-align:middle;
    }    
    .css-17m3m1o{text-align:left}
    .st-b4 {display: inline-flex}
    .stRadio{text-align:center}
    ul {
        list-style-type: square;
        text-align:left;
    }      
    mark.title {
        color:#7a44f2;
        background:none;
    }
    .e1tzin5v3{
        text-align:center}
    </style>"""
Barra_superior="""
<div class="barra-superior">
    <div class="imagen-flotar" style="height: 70px; left: 10px; padding:15px">
        <a class="imagen-flotar" style="float:left;" href="https://www.crcom.gov.co" title="CRC">
            <img src="https://www.postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png" alt="CRC" style="height:40px">
        </a>
        <a class="imagen-flotar" style="padding-left:10px;" href="https://www.postdata.gov.co" title="Postdata">
            <img src="https://www.postdata.gov.co/sites/default/files/postdata-logo.png" alt="Inicio" style="height:40px">
        </a>
    </div>
    <!--<div class="imagen-flotar" style="height: 80px; left: 300px; padding:2px">
        <a class="imagen-flotar" href="https://www.crcom.gov.co" title="CRC">
            <img src="https://raw.githubusercontent.com/postdatacrc/Reporte-de-industria/main/Iconos/banner-reporte-de-industria-980x76.png" alt="CRC" style="">
        </a>
    </div>-->    
</div>"""

##Definiciones M??vil

def DownloadMOVIL(x):
    min_down=5;max_down=25;weight_down=0.375
    if x>max_down:
        y=100*weight_down
    elif x<min_down:
        y=0
    else:    
        y= y=(x/max_down)*100*weight_down
    return y
def UploadMOVIL(x):
    min_up=2.6;max_up=12.5;weight_up=0.258
    if x>max_up:
        y=100*weight_up
    elif x<min_up:
        y=0
    else:    
        y= y=(x/max_up)*100*weight_up
    return y
def LatencyMOVIL(x):
    min_Lat=25;max_Lat=100;weight_Lat=0.184
    if x>=max_Lat:
        y=0
    elif x<=min_Lat:
        y=100*weight_Lat
    else:
        y=100*(max_Lat-x)*weight_Lat/(max_Lat-min_Lat)
    return y
def JitterMOVIL(x):
    min_Jit=0;max_Jit=50;weight_Jit=0.09
    if x>=max_Jit:
        y=0
    elif x<=min_Jit:
        y=100*weight_Jit
    else:
        y=100*(max_Jit-x)*weight_Jit/(max_Jit-min_Jit)
    return y
def AvgPacket(x):
    weight_AvgPack=0.093
    y=y=100*(100-x)*weight_AvgPack/(100)
    return y

## Definiciones Fijos

def DownloadFIJO(x):
    min_down=25;max_down=50;weight_down=0.377
    if x>max_down:
        y=100*weight_down
    elif x<min_down:
        y=0
    else:    
        y= y=(x/max_down)*100*weight_down
    return y
def UploadFIJO(x):
    min_up=5;max_up=20;weight_up=0.273
    if x>max_up:
        y=100*weight_up
    elif x<min_up:
        y=0
    else:    
        y= y=(x/max_up)*100*weight_up
    return y
def LatencyFIJO(x):
    min_Lat=25;max_Lat=100;weight_Lat=0.23
    if x>=max_Lat:
        y=0
    elif x<=min_Lat:
        y=100*weight_Lat
    else:
        y=100*(max_Lat-x)*weight_Lat/(max_Lat-min_Lat)
    return y
def JitterFIJO(x):
    min_Jit=0;max_Jit=50;weight_Jit=0.12
    if x>=max_Jit:
        y=0
    elif x<=min_Jit:
        y=100*weight_Jit
    else:
        y=100*(max_Jit-x)*weight_Jit/(max_Jit-min_Jit)
    return y

def lineatiempoMuni(df,yvalue):
    fig = make_subplots(rows=1, cols=1)
    for proveedor in df['provider'].unique().tolist():
        df2=df[df['provider']==proveedor]
        fig.add_trace(go.Scatter(x=df2['periodo'],y=df2[yvalue],name=proveedor,marker=dict(size=7,color=Colores_proveedores[proveedor]),line=dict(color=Colores_proveedores[proveedor]),
        hovertemplate =
            '<br><b>Operador</b>:<br><extra></extra>'+proveedor+
            '<br><b>Periodo</b>: %{x}<br>'+                         
            ParametroFijo+'-'+dict_parametros_unidad[ParametroFijo]+': %{y:.3f}<br>'))
    fig.update_yaxes(tickfont=dict(family='Poppins', color='black', size=16),titlefont_size=16, title_text=ParametroFijo+' '+dict_parametros_unidad[ParametroFijo], row=1, col=1)
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/a??o)',row=1, col=1
    ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
    fig.update_layout(height=550,legend_title=None)
    fig.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
    title={
    'text':'Evoluci??n '+ParametroFijo+' por operador',
    'y':0.96,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})        
    fig.update_layout(legend=dict(orientation="h",xanchor='center',y=1.05,x=0.5,font_size=11),showlegend=True)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(192, 192, 192, 0.8)')
    fig.update_layout(yaxis_tickformat ='d')
    fig.update_layout(xaxis_tickformat ='%m/%y')
    fig.add_annotation(
    showarrow=False,
    text='',
    font=dict(size=11), xref='x domain',x=0.5,yref='y domain',y=-0.2)    
    return fig

def lineatiempoMuniMovil(df,yvalue):
    fig = make_subplots(rows=1, cols=1)
    for proveedor in df['provider'].unique().tolist():
        df2=df[df['provider']==proveedor]
        fig.add_trace(go.Scatter(x=df2['periodo'],y=df2[yvalue],name=proveedor,marker=dict(color=Colores_proveedores[proveedor]),line=dict(color=Colores_proveedores[proveedor]),
        hovertemplate =
            '<br><b>Operador</b>:<br><extra></extra>'+proveedor+
            '<br><b>Periodo</b>: %{x}<br>'+                         
            ParametroMovil+'-'+dict_parametros_unidad[ParametroMovil]+': %{y:.3f}<br>'))
    fig.update_yaxes(tickfont=dict(family='Poppins', color='black', size=16),titlefont_size=16, title_text=ParametroMovil+' '+dict_parametros_unidad[ParametroMovil], row=1, col=1)
    fig.update_xaxes(tickangle=0, tickfont=dict(family='Poppins', color='black', size=14),title_text='Fecha (mes/a??o)',row=1, col=1
    ,zeroline=True,linecolor = 'rgba(192, 192, 192, 0.8)',zerolinewidth=2)
    fig.update_layout(height=550,legend_title=None)
    fig.update_layout(font_color="Black",font_family="Poppins",title_font_color="Black",titlefont_size=16,
    title={
    'text':'Evoluci??n '+ParametroMovil+' por operador',
    'y':0.96,
    'x':0.5,
    'xanchor': 'center',
    'yanchor': 'top'})        
    fig.update_layout(legend=dict(orientation="h",xanchor='center',y=1.05,x=0.5,font_size=11),showlegend=True)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(192, 192, 192, 0.8)')
    fig.update_layout(yaxis_tickformat ='d')
    fig.update_layout(xaxis_tickformat ='%m/%y')
    fig.add_annotation(
    showarrow=False,
    text='',
    font=dict(size=11), xref='x domain',x=0.5,yref='y domain',y=-0.2)    
    return fig


#@st.cache(ttl=24*3600,allow_output_mutation=True)
def ReadDataFijoMunicipios():
    FijosMuni=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/Bases/BaseFijosMunicipios.csv')
    return FijosMuni
BaseFijosMunicipios=ReadDataFijoMunicipios()
BaseFijosMunicipios['Indice_Descarga']=BaseFijosMunicipios['download_speed'].apply(DownloadFIJO)
BaseFijosMunicipios['Indice_Carga']=BaseFijosMunicipios['upload_speed'].apply(UploadFIJO)
BaseFijosMunicipios['Indice_Latencia']=BaseFijosMunicipios['latency'].apply(LatencyFIJO)
BaseFijosMunicipios['Indice_Jitter']=BaseFijosMunicipios['jitter'].apply(JitterFIJO)
BaseFijosMunicipios['Indice_CRC']=BaseFijosMunicipios['Indice_Descarga']+BaseFijosMunicipios['Indice_Carga']+BaseFijosMunicipios['Indice_Latencia']+BaseFijosMunicipios['Indice_Jitter']
BaseFijosMunicipios[['download_speed','upload_speed','latency','jitter','Indice_CRC']]=BaseFijosMunicipios[['download_speed','upload_speed','latency','jitter','Indice_CRC']]
BaseFijosMunicipios['municipio']=BaseFijosMunicipios['municipio'].apply(lambda x:unidecode.unidecode(x).upper())
BaseFijosMunicipios['departamento']=BaseFijosMunicipios['departamento'].apply(lambda x:unidecode.unidecode(x).upper())
BaseFijosMunicipios['departamento']=BaseFijosMunicipios['departamento'].replace({'CAUCA DEPARTMENT':'CAUCA','NORTH SANTANDER':'NORTE DE SANTANDER',
                                                                        'SAN ANDRES AND PROVIDENCIA':'SAN ANDRES','SANTANDER DEPARTMENT':'SANTANDER',
                                                                        'BOGOTA':'BOGOTA, D.C.','NARINO':'NARI??O'})

#@st.cache(ttl=24*3600,allow_output_mutation=True)
def ReadDataMovilesMunicipios():
    MovilesMuni=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/Bases/BaseMovilesMunicipio.csv')
    return MovilesMuni
BaseMovilesMunicipio=ReadDataMovilesMunicipios()
BaseMovilesMunicipio[['download_speed','upload_speed','latency','jitter']]=round(BaseMovilesMunicipio[['download_speed','upload_speed','latency','jitter']],3)
BaseMovilesMunicipio['Indice_Descarga']=BaseMovilesMunicipio['download_speed'].apply(DownloadMOVIL)
BaseMovilesMunicipio['Indice_Carga']=BaseMovilesMunicipio['upload_speed'].apply(UploadMOVIL)
BaseMovilesMunicipio['Indice_Latencia']=BaseMovilesMunicipio['latency'].apply(LatencyMOVIL)
BaseMovilesMunicipio['Indice_Jitter']=BaseMovilesMunicipio['jitter'].apply(JitterMOVIL)
BaseMovilesMunicipio['Indice_AvgPack']=BaseMovilesMunicipio['AvgPack'].apply(AvgPacket)
BaseMovilesMunicipio['Indice_CRC']=BaseMovilesMunicipio['Indice_Descarga']+BaseMovilesMunicipio['Indice_Carga']+BaseMovilesMunicipio['Indice_Latencia']+BaseMovilesMunicipio['Indice_Jitter']+BaseMovilesMunicipio['Indice_AvgPack']
BaseMovilesMunicipio['municipio']=BaseMovilesMunicipio['municipio'].apply(lambda x:unidecode.unidecode(x).upper())
BaseMovilesMunicipio['departamento']=BaseMovilesMunicipio['departamento'].apply(lambda x:unidecode.unidecode(x).upper())
BaseMovilesMunicipio['departamento']=BaseMovilesMunicipio['departamento'].replace({'CAUCA DEPARTMENT':'CAUCA','NORTH SANTANDER':'NORTE DE SANTANDER',
                                                                        'SAN ANDRES AND PROVIDENCIA':'SAN ANDRES','SANTANDER DEPARTMENT':'SANTANDER',
                                                                        'BOGOTA':'BOGOTA, D.C.','NARINO':'NARI??O'})

#@st.cache(allow_output_mutation=True)
def MunicipiosColombia():
    gdf= gpd.read_file("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/co_2018_MGN_MPIO_POLITICO.geojson")
    gdf=gdf.rename(columns={'MPIO_CNMBR':'municipio','MPIO_CCNCT':'ID_MUNICIPIO','DPTO_CNMBR':'departamento'})
    gdf['municipio']=gdf['municipio'].apply(lambda x:unidecode.unidecode(x))
    gdf['departamento']=gdf['departamento'].apply(lambda x:unidecode.unidecode(x))
    gdf['departamento']=gdf['departamento'].replace({'ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA':'SAN ANDRES','NARINO':'NARI??O'})
    gdf['municipio']=gdf['municipio'].replace('BOGOTA, D.C.','BOGOTA')
    return gdf
gdf=MunicipiosColombia()
#@st.cache(allow_output_mutation=True)
def data_MuniColombia():    
    with urllib.request.urlopen("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/co_2018_MGN_MPIO_POLITICO.geojson") as url:
        Muni = json.loads(url.read().decode())
    return Muni
Colombian_MUNI=data_MuniColombia()  
Proveedores_fijo=['All Providers Combined','Claro','Tigo','Movistar','ETB','DIRECTV']    
Proveedores_moviles=['All Providers Combined','Movistar','Claro','Tigo','Avantel','WOM']
Colores_proveedores={'All Providers Combined':'black','Claro':'rgb(226,36,46)','Tigo':'rgb(57,107,80)','Movistar':'rgb(102,206,0)','ETB':'rgb(11,52,104)',
                          'DIRECTV':'rgb(0,147,209)','Avantel':'rgb(255,0,156)','WOM':'rgb(69,7,82)'}
    
st.markdown(Estilo_css+Barra_superior,unsafe_allow_html=True)

st.sidebar.markdown(r"""<b style="font-size: 26px;text-align:center;color:white"><center>??ndice de calidad<br>CRC</center></b> """,unsafe_allow_html=True)
st.sidebar.markdown(r"""<hr style='border:1px solid white'>""",unsafe_allow_html=True)
st.sidebar.markdown("""<b style='color:white'>??ndice</b>""", unsafe_allow_html=True)
select_seccion = st.sidebar.selectbox('',
                                    ['Manual','??ndice de calidad'])   


reemplazo_Muni={'SANTA FE DE ANTIOQUIA':'SANTAFE DE ANTIOQUIA','BOGOTA, D.C.':'BOGOTA','CUASPUD CARLOSAMA':'CUASPUD',
                'SOTARA - PAISPAMBA':'SOTARA','EL CANTON DEL SAN PABLO':'CANTON DEL SAN PABLO'}
                
capitales_departamento={'AMAZONAS':'LETICIA','ANTIOQUIA':'MEDELLIN','ARAUCA':'ARAUCA','ATLANTICO':'BARRANQUILLA','BOGOTA, D.C.':'BOGOTA',
                        'BOLIVAR':'CARTAGENA','BOYACA':'TUNJA','CALDAS':'MANIZALES','CAQUETA':'FLORENCIA','CASANARE':'YOPAL','CAUCA':'POPAYAN',
                        'CESAR':'VALLEDUPAR','CHOCO':'QUIBDO','CORDOBA':'MONTERIA','GUAINIA':'INIRIDA','GUAVIARE':'SAN JOSE DEL GUAVIARE',
                        'HUILA':'NEIVA','LA GUAJIRA':'RIOHACHA','MAGDALENA':'SANTA MARTA','META':'VILLAVICENCIO','NARI??O':'PASTO',
                        'NORTE DE SANTANDER':'CUCUTA','PUTUMAYO':'MOCOA','QUINDIO':'RISARALDA','SAN ANDRES':'SAN ANDRES','SANTANDER':'BUCARAMANGA',
                        'SUCRE':'SINCELEJO','TOLIMA':'IBAGUE','VALLE DEL CAUCA':'CALI','VAUPES':'MITU','VICHADA':'PUERTO CARRENO'}                

if select_seccion=='Manual':
    st.title("Manual del ??ndice de calidad CRC")   
    seccion_manual=st.radio('',['Objetivo','Justificaci??n','Metodolog??a'],horizontal=True)
    st.markdown(r"""<hr>""",unsafe_allow_html=True)
    if seccion_manual=='Objetivo':   
        st.markdown("<center><h2>Objetivo</h2></center>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:justify'>Con ocasi??n del proyecto de ???Revisi??n de las condiciones de calidad en la prestaci??n de los servicios de telecomunicaciones??? , se expidi?? la Resoluci??n CRC 6890 de 2022, desde la cual, entre otras medidas, se moderniz?? la metodolog??a de medici??n de la calidad del servicio de Internet prestado a trav??s de redes de acceso m??vil y fijo. Teniendo en cuenta lo anterior, y con el fin de incentivar la mejora continua de la calidad de los citados servicios que se prestan a los usuarios, la CRC plantea brindar informaci??n de aquellas ciudades que cuentan con las mejores condiciones en t??rminos de calidad del servicio que experimenta el usuario.</p>",unsafe_allow_html=True)
    elif seccion_manual=='Justificaci??n':
        st.markdown("<center><h2>Justificaci??n</h2></center>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:justify'>Para la recopilar la informaci??n de las mediciones de calidad, se utiliz?? la metodolog??a crowdsourcing, mediante la cual se logr?? obtener las mediciones directamente desde los dispositivos que los usuarios utilizan para acceder a los servicios de Internet m??vil e Internet fijo. Por lo anterior, las evaluaciones comparativas, y calificaciones entre operadores de redes m??viles, son de gran importancia, pues en su gran mayor??a, utilizan estos resultados con el fin de impulsar su identidad corporativa, no obstante, es menester garantizar la transparencia de la informaci??n publicada y que carezca de sesgos (ETSI TR 103 559) , por lo que, aunado a lo anterior, el prop??sito tambi??n es trabajar en la reducci??n de la asimetr??a de la informaci??n hacia el usuario, de tal manera que pueda tomar decisiones bien informado, respecto de la contrataci??n de los servicios de Internet m??vil e Internet fijo. </p>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:justify'>Dicho objetivo se puede lograr mediante la definici??n de un ?????ndice de Calidad de la Experiencia -ICE???, con la finalidad principal de identificar, el posicionamiento de las ciudades seg??n la calidad de la experiencia percibida, en un lenguaje sencillo y de f??cil entendimiento. Considerando que el despliegue de redes m??viles y fijas a nivel nacional var??a entre los operadores, pues las redes se construyen con diferentes objetivos de cobertura, y que precisamente este aspecto, junto con indicadores como la velocidad de descarga, la velocidad de carga, la latencia, el jitter y la tasa de p??rdida de paquetes, suelen ser factores importantes que influyen en la toma de decisiones de los usuarios sobre el operador que mejor se ajusta a sus necesidades, por lo que la evaluaci??n comparativa debe considerar las diferencias entre los citados par??metros en los resultados. El reporte t??cnico ETSI TR 103 559, analiza la construcci??n y la metodolog??a de una evaluaci??n comparativa en una medici??n nacional, considerando aspectos como el ??rea y la poblaci??n a cubrir, la recopilaci??n y agregaci??n de las mediciones, y la ponderaci??n de los diversos aspectos considerados, con el principal prop??sito de identificar las mejores pr??cticas que se deben tener en cuenta a la hora de realizar una evaluaci??n comparativa de las redes m??viles, de tal manera que la comparaci??n refleje la verdadera experiencia del usuario.Considerando las recomendaciones y buenas pr??cticas contenidas en el mencionado reporte t??cnico de la ETSI, la presente evaluaci??n comparativa se fundamenta b??sicamente en dos aspectos importantes: una caracterizaci??n de par??metros, y una definici??n de valores que permiten la normalizaci??n y los correspondientes ponderadores.</p>",unsafe_allow_html=True)
    elif seccion_manual=='Metodolog??a':
        st.markdown("<center><h2>Metodolog??a</h2></center>",unsafe_allow_html=True)
        st.markdown("<p style='text-align:justify'>Para la caracterizaci??n de indicadores, la referencia directa es la Resoluci??n CRC 6890 de 2022, desde la cual se establecieron la velocidad de descarga, la velocidad de carga, la latencia, el jitter y la tasa de p??rdida de paquetes para medir la calidad del servicio de Internet m??vil. En cuanto al servicio de Internet fijo se plantean los indicadores de velocidad de descarga, velocidad de carga, latencia y el jitter.Los valores de los indicadores para la normalizaci??n (m??ximos y m??nimos) del servicio de Internet m??vil est??n basados en los valores objetivo definidos en la Resoluci??n CRC 6890 de 2022. Para la ponderaci??n de estos indicadores, se realiz?? un ejercicio de encuesta desde la perspectiva de usuarios para definir el peso (Ponderaci??n) de cada indicador.El c??lculo del ICE est?? conformado por la sumatoria de la relaci??n del valor de la medici??n y el valor de normalizaci??n y el producto con el ponderador de cada uno de los indicadores.</p>",unsafe_allow_html=True)    
        col1,col2=st.columns(2)
        with col1:
            st.markdown("<p style='font-size:11px;text-align:center'><b>Tabla 1:</b> Valores de referencia para el c??lculo del ICE para el servicio de Internet m??vil</p>",unsafe_allow_html=True)
            st.image("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/ICE%20Movil.png")
        with col2:
            st.markdown("<p style='font-size:11px;text-align:center'><b>Tabla 2:</b> Valores de referencia para el c??lculo del ICE para el servicio de Internet fijo</p>",unsafe_allow_html=True)
            st.image("https://raw.githubusercontent.com/postdatacrc/IndiceCRC/main/ICE%20Fijo.png")
        
if select_seccion=='??ndice de calidad':
    st.title("??ndice de calidad CRC") 
    select_servicio=st.radio('Seleccione un servicio para el c??lculo del indicador',['Servicios fijos','Servicios m??viles'],horizontal=True)
    st.markdown(r"""<hr>""",unsafe_allow_html=True)
    
    if select_servicio=='Servicios fijos':
        st.markdown("<center><h2>Servicios fijos</h2></center>",unsafe_allow_html=True)
        puebaBaseFijosMuni=gdf.merge(BaseFijosMunicipios,left_on=['municipio','departamento'],right_on=['municipio','departamento'])        

        dict_parametros={'Velocidad de descarga':'download_speed','Velocidad de carga':'upload_speed','Latencia':'latency','Jitter':'jitter','??ndice calidad':'Indice_CRC'}
        dict_parametros_unidad={'Velocidad de descarga':'(mpbs)','Velocidad de carga':'(mbps)','Latencia':'(ms)','Jitter':'(ms)','??ndice calidad':'(%)'}
        ParametroFijo=st.radio('Elija un par??metro a calcular',['Velocidad de descarga','Velocidad de carga','Latencia','Jitter','??ndice calidad'],horizontal=True)        
        # prueba1=st.selectbox('',BaseFijosMunicipios['municipio'].unique().tolist())
        # prueba2=st.selectbox('',gdf['municipio'].unique().tolist())
        # st.markdown(list(set(puebaBaseFijosMuni['municipio'].unique().tolist()).symmetric_difference(BaseFijosMunicipios['municipio'].unique().tolist())))
        col1,col2,col3=st.columns(3)
        with col2:
            select_dimAnalisis=st.selectbox('Tipo de an??lisis de los indicadores',['An??lisis por municipio','An??lisis por operador'])
        st.markdown(r"""<hr>""",unsafe_allow_html=True)
        DepartamentosFijos=sorted(BaseFijosMunicipios['departamento'].unique().tolist())
        
        if select_dimAnalisis=='An??lisis por municipio':
            col1,col2=st.columns(2)
            with col1:
                Dept_fijo=st.selectbox('Escoja el departamento',DepartamentosFijos,4)
            with col2:    
                Municipiosfijo=sorted(BaseFijosMunicipios[BaseFijosMunicipios['departamento']==Dept_fijo]['municipio'].unique().tolist())
                poscapital=Municipiosfijo.index(capitales_departamento[Dept_fijo])
                Muni_fijo=st.selectbox('Escoja el municipio',Municipiosfijo,poscapital)            
                        
            FijoMuniMetric=BaseFijosMunicipios[(BaseFijosMunicipios['municipio']==Muni_fijo)&(BaseFijosMunicipios['periodo']=='2021-12')&(BaseFijosMunicipios['provider']=='All Providers Combined')]
            dfFijoMuni=BaseFijosMunicipios[(BaseFijosMunicipios['municipio']==Muni_fijo)&(BaseFijosMunicipios['departamento']==Dept_fijo)]
                        
            if FijoMuniMetric.empty==True:
                st.info('Este municipio no tiene valores en diciembre de 2021') 
            else:    
                st.markdown("<center><h3>Valores promedios obtenidos en el periodo 2021-12</h3></center>",unsafe_allow_html=True)
                col1,col2,col3,col4,col5=st.columns(5)            
                with col1:
                    st.markdown("<center><h5>Velocidad descarga<br>(mpbs)</h5></center>",unsafe_allow_html=True)               
                with col2:
                    st.markdown("<center><h5>Velocidad carga<br>(mpbs)</h5></center>",unsafe_allow_html=True)
                with col3:
                    st.markdown("<center><h5>Latencia<br>(ms)</h5></center>",unsafe_allow_html=True)
                with col4:
                    st.markdown("<center><h5>Jitter<br>(ms)</h5></center>",unsafe_allow_html=True)
                with col5:
                    st.markdown("<center><h5>??ndice CRC<br>(%)</h5></center>",unsafe_allow_html=True)
                col1,col2,col3,col4,col5=st.columns(5)                
                with col1:
                    st.markdown(str(round(FijoMuniMetric['download_speed'].values.tolist()[0],2)))     
                with col2:
                    st.markdown(str(round(FijoMuniMetric['upload_speed'].values.tolist()[0],2)))     
                with col3:
                    st.markdown(str(round(FijoMuniMetric['latency'].values.tolist()[0],2)))     
                with col4:
                    st.markdown(str(round(FijoMuniMetric['jitter'].values.tolist()[0],2)))     
                with col5:
                    st.markdown(str(round(FijoMuniMetric['Indice_CRC'].values.tolist()[0],2)))           
                        
            dfFijoMuni2=dfFijoMuni[['periodo','municipio','departamento','provider',dict_parametros[ParametroFijo]]]
            col1,col2=st.columns(2)
            st.plotly_chart(lineatiempoMuni(dfFijoMuni2[dfFijoMuni2['provider'].isin(Proveedores_fijo)],dict_parametros[ParametroFijo]),use_container_width=True)

        if select_dimAnalisis=='An??lisis por operador':
            col1,col2=st.columns([4,1])
            with col1:
                select_operadorFijo=st.radio('Seleccione el operador',Proveedores_fijo,horizontal=True)
            puebaBaseFijosMuni['ID_MUNICIPIO']=puebaBaseFijosMuni['ID_MUNICIPIO'].astype('str')
            with col2:
                select_periodoFijo=st.selectbox('Escoja el periodo',puebaBaseFijosMuni['periodo'].unique().tolist()[::-1],0)
            color_mapa={'Velocidad de descarga':'RdYlGn','Velocidad de carga':'RdYlGn','Latencia':'RdYlGn_r','Jitter':'RdYlGn_r','??ndice calidad':'RdYlGn'}    
            colombia_map = folium.Map(width='100%',location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
            tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
            for tile in tiles:
                folium.TileLayer(tile).add_to(colombia_map)
            choropleth=folium.Choropleth(
                geo_data=Colombian_MUNI,
                data=puebaBaseFijosMuni[(puebaBaseFijosMuni['periodo']==select_periodoFijo)&(puebaBaseFijosMuni['provider']==select_operadorFijo)],
                columns=['ID_MUNICIPIO',dict_parametros[ParametroFijo]],
                key_on='feature.properties.MPIO_CCNCT',
                fill_color=color_mapa[ParametroFijo], 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name=ParametroFijo+' '+dict_parametros_unidad[ParametroFijo]+' '+select_periodoFijo,
                smooth_factor=0).add_to(colombia_map)
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['MPIO_CNMBR'], style=style_function, labels=False))
            folium.LayerControl().add_to(colombia_map)

            #Adicionar valores 
            style_function = lambda x: {'fillColor': '#ffffff', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.1, 
                                        'weight': 0.1}
            highlight_function = lambda x: {'fillColor': '#000000', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.50, 
                                            'weight': 0.1}
            NIL = folium.features.GeoJson(
                data = puebaBaseFijosMuni[(puebaBaseFijosMuni['periodo']==select_periodoFijo)&(puebaBaseFijosMuni['provider']==select_operadorFijo)],
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['municipio','ID_MUNICIPIO','departamento',dict_parametros[ParametroFijo]],
                    aliases=['Municipio','ID','departamento',ParametroFijo],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            colombia_map.add_child(NIL)
            colombia_map.keep_in_front(NIL)
            col1,col2,col3=st.columns([1,2,1])
            with col2:
                folium_static(colombia_map,width=480) 
       
    if select_servicio=='Servicios m??viles':
        st.markdown("<center><h2>Servicios m??viles</h2></center>",unsafe_allow_html=True)        
        puebaBaseMovilesMuni=gdf.merge(BaseMovilesMunicipio,left_on=['municipio','departamento'],right_on=['municipio','departamento'])        

        dict_parametros={'Velocidad de descarga':'download_speed','Velocidad de carga':'upload_speed','Latencia':'latency','Jitter':'jitter','??ndice calidad':'Indice_CRC'}
        dict_parametros_unidad={'Velocidad de descarga':'(mpbs)','Velocidad de carga':'(mbps)','Latencia':'(ms)','Jitter':'(ms)','??ndice calidad':'(%)'}
        ParametroMovil=st.radio('Elija un par??metro a calcular',['Velocidad de descarga','Velocidad de carga','Latencia','Jitter','??ndice calidad'],horizontal=True)        

        col1,col2,col3=st.columns(3)
        with col2:
            select_dimAnalisis=st.selectbox('Tipo de an??lisis de los indicadores',['An??lisis por municipio','An??lisis por operador'])
        st.markdown(r"""<hr>""",unsafe_allow_html=True)
        DepartamentosMovil=sorted(BaseMovilesMunicipio['departamento'].unique().tolist())

        if select_dimAnalisis=='An??lisis por municipio':
            col1,col2=st.columns(2)
            with col1:
                Dept_Movil=st.selectbox('Escoja el departamento',DepartamentosMovil,4)
            with col2:    
                Municipiosmovil=sorted(BaseMovilesMunicipio[BaseMovilesMunicipio['departamento']==Dept_Movil]['municipio'].unique().tolist())
                poscapital=Municipiosmovil.index(capitales_departamento[Dept_Movil])
                Muni_movil=st.selectbox('Escoja el municipio',Municipiosmovil,poscapital)            
                        
            MovilMuniMetric=BaseMovilesMunicipio[(BaseMovilesMunicipio['municipio']==Muni_movil)&(BaseMovilesMunicipio['periodo']=='2021-12')&(BaseMovilesMunicipio['provider']=='All Providers Combined')]
            dfMovilMuni=BaseMovilesMunicipio[(BaseMovilesMunicipio['municipio']==Muni_movil)&(BaseMovilesMunicipio['departamento']==Dept_Movil)]
                        
            if MovilMuniMetric.empty==True:
                st.info('Este municipio no tiene valores en diciembre de 2021') 
            else:    
                st.markdown("<center><h3>Valores promedios obtenidos en el periodo 2021-12</h3></center>",unsafe_allow_html=True)
                col1,col2,col3,col4,col5=st.columns(5)            
                with col1:
                    st.markdown("<center><h5>Velocidad descarga<br>(mpbs)</h5></center>",unsafe_allow_html=True)               
                with col2:
                    st.markdown("<center><h5>Velocidad carga<br>(mpbs)</h5></center>",unsafe_allow_html=True)
                with col3:
                    st.markdown("<center><h5>Latencia<br>(ms)</h5></center>",unsafe_allow_html=True)
                with col4:
                    st.markdown("<center><h5>Jitter<br>(ms)</h5></center>",unsafe_allow_html=True)
                with col5:
                    st.markdown("<center><h5>??ndice CRC<br>(%)</h5></center>",unsafe_allow_html=True)
                col1,col2,col3,col4,col5=st.columns(5)                
                with col1:
                    st.markdown(str(round(MovilMuniMetric['download_speed'].values.tolist()[0],2)))     
                with col2:
                    st.markdown(str(round(MovilMuniMetric['upload_speed'].values.tolist()[0],2)))     
                with col3:
                    st.markdown(str(round(MovilMuniMetric['latency'].values.tolist()[0],2)))     
                with col4:
                    st.markdown(str(round(MovilMuniMetric['jitter'].values.tolist()[0],2)))     
                with col5:
                    st.markdown(str(round(MovilMuniMetric['Indice_CRC'].values.tolist()[0],2)))           
                        
            dfMovilMuni2=dfMovilMuni[['periodo','municipio','departamento','provider',dict_parametros[ParametroMovil]]]
            col1,col2=st.columns(2)
            st.plotly_chart(lineatiempoMuniMovil(dfMovilMuni2[dfMovilMuni2['provider'].isin(Proveedores_moviles)],dict_parametros[ParametroMovil]),use_container_width=True)

        if select_dimAnalisis=='An??lisis por operador':        
            col1,col2=st.columns([4,1])
            with col1:
                select_operadorMovil=st.radio('Seleccione el operador',Proveedores_moviles,horizontal=True)
            puebaBaseMovilesMuni['ID_MUNICIPIO']=puebaBaseMovilesMuni['ID_MUNICIPIO'].astype('str')
            with col2:
                select_periodoMovil=st.selectbox('Escoja el periodo',puebaBaseMovilesMuni['periodo'].unique().tolist()[::-1],0)
            if puebaBaseMovilesMuni[(puebaBaseMovilesMuni['periodo']==select_periodoMovil)&(puebaBaseMovilesMuni['provider']==select_operadorMovil)].empty==True:
                st.info('Este operador no tiene valores para el periodo seleccionado')
            else:        
                color_mapa={'Velocidad de descarga':'RdYlGn','Velocidad de carga':'RdYlGn','Latencia':'RdYlGn_r','Jitter':'RdYlGn_r','??ndice calidad':'RdYlGn'}    
                colombia_map = folium.Map(width='100%',location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
                tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
                for tile in tiles:
                    folium.TileLayer(tile).add_to(colombia_map)
                choropleth=folium.Choropleth(
                    geo_data=Colombian_MUNI,
                    data=puebaBaseMovilesMuni[(puebaBaseMovilesMuni['periodo']==select_periodoMovil)&(puebaBaseMovilesMuni['provider']==select_operadorMovil)],
                    columns=['ID_MUNICIPIO',dict_parametros[ParametroMovil]],
                    key_on='feature.properties.MPIO_CCNCT',
                    fill_color=color_mapa[ParametroMovil], 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name=ParametroMovil+' '+dict_parametros_unidad[ParametroMovil]+' '+select_periodoMovil,
                    smooth_factor=0).add_to(colombia_map)
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth.geojson.add_child(
                    folium.features.GeoJsonTooltip(['MPIO_CNMBR'], style=style_function, labels=False))
                folium.LayerControl().add_to(colombia_map)

                #Adicionar valores 
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                highlight_function = lambda x: {'fillColor': '#000000', 
                                                'color':'#000000', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                NIL = folium.features.GeoJson(
                    data = puebaBaseMovilesMuni[(puebaBaseMovilesMuni['periodo']==select_periodoMovil)&(puebaBaseMovilesMuni['provider']==select_operadorMovil)],
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['municipio','ID_MUNICIPIO','departamento',dict_parametros[ParametroMovil]],
                        aliases=['Municipio','ID','departamento',ParametroMovil],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                colombia_map.add_child(NIL)
                colombia_map.keep_in_front(NIL)
                col1,col2,col3=st.columns([1,2,1])
                with col2:
                    folium_static(colombia_map,width=480) 
        