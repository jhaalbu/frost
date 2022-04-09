import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
from streamlit_folium import folium_static
import folium
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from st_aggrid.shared import GridUpdateMode

client_id = 'b8b1793b-27ff-4f4d-a081-fcbcc5065b53'
client_secret = '7f24c0ca-ca82-4ed6-afcd-23e657c2e78c'

parametere = [
   'mean(surface_snow_thickness P1M)',
   'mean(surface_snow_thickness P3M)',
   'mean(surface_snow_thickness PT1H)',
   'min(surface_snow_thickness P1M)',
   'min(surface_snow_thickness P3M)',
   'max(surface_snow_thickness P1M)',
   'max(surface_snow_thickness P3M)',
   'cloud_area_fraction',
   'best_estimate_mean(air_temperature_anomaly P1M 1991_2020)',
   'air_temperature',
   'best_estimate_max(air_temperature P1D)',
   'best_estimate_mean(air_temperature P1D)',
   'best_estimate_mean(air_temperature P1M)',
   'best_estimate_mean(air_temperature P1Y)',
   'best_estimate_mean(air_temperature P3M)',
   'best_estimate_mean(air_temperature_anomaly P1Y 1991_2020)',
   'best_estimate_mean(air_temperature_anomaly P3M 1991_2020)',
   'best_estimate_min(air_temperature P1D)',
   'sum(precipitation_amount P1D)',
   'sum(precipitation_amount P1M)',
   'sum(precipitation_amount P1Y)',
   'sum(precipitation_amount P3M)',
   'sum(precipitation_amount P6M)',
   'sum(precipitation_amount P30D)',
   'sum(precipitation_amount PT1H)',
   'max(sum(precipitation_amount P1D) P1M)',
   'number_of_days_gte(sum(precipitation_amount P1D) P1M 1.0)',
   'number_of_days_gte(sum(precipitation_amount_normal P1D 1991_2020) P1Y 1.0)',
   'over_time(sum(time_of_maximum_precipitation_amount P1D) P1M)',
   'sum(precipitation_amount PT12H)',
   'sum(precipitation_amount_anomaly P1M 1971_2000)',
   'sum(precipitation_amount_anomaly P1M 1991_2020)',
   'sum(precipitation_amount_normal P1Y 1991_2020)',
   'max(wind_speed PT1H)',
   'max(wind_speed_of_gust PT1H)',
   'max_wind_speed(wind_from_direction PT1H)',
   'max_wind_speed(wind_from_direction_of_gust PT1H)',
   'wind_from_direction',
   'wind_from_direction_of_gust',
   'wind_speed',
   'wind_speed_of_gust'
]

import frost2df # for frost.help
from frost2df import frost2df, obs2df, lightning2df, codetable



@st.cache
def hent_stasjoner(fylke):
    df_stasjoner = frost2df('sources', {'county': kommune})
    #df_stasjoner['validFrom'] = pd.to_datetime(df_stasjoner['validFrom'], format="%Y-%m-%d")
    #mask = (df_stasjoner['validFrom'] > '1700-01-01') & (df_stasjoner['validFrom'] <= stasjonsvarighet)
    #df_utvalg= df_stasjoner.loc[mask]
    #df_utvalg.reset_index(inplace=True)
    #AgGrid(df_utvalg)
    return df_stasjoner

@st.cache
def hent_parametere(stasjon):
    raadata = frost2df('observations/availableTimeSeries', {'sources': utvalg["selected_rows"][0]["id"]})
    data = raadata[raadata['elementId'].isin(parametere)]
    return data

@st.cache
def hent_data(parametre):
    #data = obs2df(parameters=parameters, verbose=True)
    data = frost2df('observations', parameters)
    return data

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("multiple")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

def callback_knapp1():
    st.session_state.knapp = True
    st.session_state.knapp2 = False
    st.session_state.knapp2 = False
def callback_knapp2():
    st.session_state.knapp2 = True
    st.session_state.knapp3 = False
def callback_knapp3():
    if st.session_state.knapp3 == False:
        st.session_state.knapp3 = True
    else:
        st.session_state.knapp3 = False


def convert_df(df):
   return df.to_csv().encode('utf-8')


kommune = st.text_input("Fylke", "Vestland")
#stasjonsvarighet = st.text_input('Oppstart stasjon:', '1990-01-01')

if 'knapp' not in st.session_state:
    st.session_state.knapp = False

if 'knapp2' not in st.session_state:
    st.session_state.knapp2 = False

st.button(label = 'Vis stasjoner', on_click=callback_knapp1)



if st.session_state.knapp:
    df_utvalg = hent_stasjoner(kommune)
    
    #TODO: Bruke @st.cache
    #st.session_state.knapp = True

    #st.write(utvalg)
    #st.write(utvalg["selected_rows"][0]["id"])
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
    utvalg = aggrid_interactive_table(df_utvalg)
    #stasjon = st.text_input('Stasjonsnr', 'SN59450')

    st.button(label = 'Vis alle parameter', on_click=callback_knapp2)
    #st.button(label = 'Vis utvalgte parameter', on_click=callback_knapp2)
    #Må bruke session state her

    #Vise kva parameter som finnes på stasjonen, eller vise dette lenger oppe?
    if st.session_state.knapp2:
        df_parametere = hent_parametere(utvalg["selected_rows"][0]["id"])
        
        selection = aggrid_interactive_table(df_parametere)

   

        selct_dict = selection["selected_rows"][0]

        sources = st.text_input("Source", selct_dict['sourceId'])
        elements = st.text_input("Element", selct_dict["elementId"])
        validfrom = st.text_input("Element", selct_dict["validFrom"])
        validto = st.text_input("Element", '2024-05-17')
        parameters = {
            'sources': sources,
            'elements': elements,
            'referencetime': validfrom + '/' + validto,
            'timeoffsets': selct_dict["timeOffset"],
            'timeresolutions': selct_dict["timeResolution"] 
            
        }

        st.button(label = "Vis data", on_click=callback_knapp3)
        
        if st.session_state.knapp3:

        
#'timeresolution': selct_dict["timeResolution"] + '/2024-05-17'
            AgGrid(hent_data(parameters))
        #st.write(df_parameter)
            csv = convert_df(hent_data(parameters))

            st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )

    #Velge ut parameter

    #Velge om det skal lastes ned, eller plottes