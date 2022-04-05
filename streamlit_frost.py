import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
from streamlit_folium import folium_static
import folium
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

import frost2df # for frost.help
from frost2df import frost2df, obs2df, lightning2df, codetable

client_id = 'b8b1793b-27ff-4f4d-a081-fcbcc5065b53'
client_secret = '7f24c0ca-ca82-4ed6-afcd-23e657c2e78c'

kommune = st.text_input("Fylke", "Vestland")
stasjonsvarighet = st.text_input('Oppstart stasjon:', '1990-01-01')

def callback_knapp1():
    st.session_state.knapp = True
    st.session_state.knapp2 = False
    st.session_state.knapp2 = False
def callback_knapp2():
    st.session_state.knapp2 = True
    st.session_state.knapp3 = False
def callback_knapp3():
    st.session_state.knapp3 = True

def convert_df(df):
   return df.to_csv().encode('utf-8')


if 'knapp' not in st.session_state:
    st.session_state.knapp = False

if 'knapp2' not in st.session_state:
    st.session_state.knapp2 = False

st.button(label = 'Vis stasjoner', on_click=callback_knapp1)

if st.session_state.knapp:
    #st.session_state.knapp = True
    df_stasjoner = frost2df('sources', {'county': kommune})
    df_stasjoner['validFrom'] = pd.to_datetime(df_stasjoner['validFrom'], format="%Y-%m-%d")
    mask = (df_stasjoner['validFrom'] > '1700-01-01') & (df_stasjoner['validFrom'] <= stasjonsvarighet)
    df_utvalg= df_stasjoner.loc[mask]
    df_utvalg.reset_index(inplace=True)
    AgGrid(df_utvalg)

    m = folium.Map(location=[df_utvalg['geometry.coordinates'][0][1], df_utvalg['geometry.coordinates'][0][0]], zoom_start=8) #Bruker transformerte koordinater (ikkej funne ut korleis bruke UTM med folium)

    for i in range(len(df_utvalg)):
        folium.Marker(
            location=[df_utvalg['geometry.coordinates'][i][1], df_utvalg['geometry.coordinates'][i][0]],
            popup=df_utvalg['name'][i] + ' | ' + df_utvalg['id'][i] + ' | ' + str(df_utvalg['validFrom'][i]),
            icon=folium.Icon(color="green")
        ).add_to(m)
    #Legger til Norgeskart WMS

    folium.raster_layers.WmsTileLayer(
        url='https://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=topo4&zoom={z}&x={x}&y={y}',
        name='Norgeskart',
        max_bounds=True,
        fmt='image/png',
        layers='topo4',
        attr=u'<a href="http://www.kartverket.no/">Kartverket</a>',
        transparent=True,
        overlay=True,
        control=True,
        
    ).add_to(m)

    folium_static(m)

    stasjon = st.text_input('Stasjonsnr', 'SN59450')

    st.button(label = 'Vis parameter', on_click=callback_knapp2)
    #Må bruke session state her

    #Vise kva parameter som finnes på stasjonen, eller vise dette lenger oppe?
    if st.session_state.knapp2:

        AgGrid(frost2df('observations/availableTimeSeries', {'sources': stasjon}))

        element = st.text_input('Element', 'wind_From_direction')
        time_offset = st.text_input('Time Offset', 'PT0H')
        valid_from = st.text_input('Dato fra', '2014-04-03')
        valid_to = st.text_input('Dato til', '2024-04-03')
        timeresolution = st.text_input('Tidsoppløsning', 'PT1H')

        st.button(label = "Vis resultat", on_click=callback_knapp3)

        if st.session_state.knapp3:

            parameters = {
                'sources': stasjon,
                'elements': element,
                'referencetime': valid_from + '/' + valid_to,
                'timeoffsets': time_offset,
                'timeresolution': timeresolution 
            }
            df_para = obs2df(parameters=parameters, verbose=True).copy()

            AgGrid(df_para)
        #st.write(df_parameter)
            csv = convert_df(df_para)

            st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )
    #Velge ut parameter

    #Velge om det skal lastes ned, eller plottes