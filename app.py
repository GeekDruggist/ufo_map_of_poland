from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import dash_leaflet as dl


external_css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

country = './assets/maps_geojson/country.geojson'
voivodeships = './assets/maps_geojson/voivodeships.geojson'
counties = './assets/maps_geojson/counties.geojson'

icon = {
    'iconUrl': './assets/icons/ufo-flying.png',
    # 'shadowUrl':"",
    'iconSize': [20, 20],
    # 'shadowSize': [50, 64],
    # 'iconAnchor': [22, 94],
    # 'shadowAnchor': [4, 62],
    # 'popupAnchor':[-3, -76],
}


DATA = pd.read_csv('./assets/data/Clean_data.csv')
V_COORDS =  pd.read_csv('./assets/data/Voivod_coords.csv')

year = pd.to_datetime(DATA['Sighted on']).dt.strftime('%Y')

initial_lat = float(DATA[DATA['Year'] == DATA['Year'].min()]['Lat'])
initial_long = float(DATA[DATA['Year'] == DATA['Year'].min()]['Long'])



app = Dash(external_stylesheets=[external_css], prevent_initial_callbacks='initial_duplicate')

app.layout = html.Div([
                        html.Div(
                            [html.H1(children='UFO / UAP map of Poland')], className='app_container'),

                            # year slider:
                            html.Div(dcc.Slider(

                                min=int(year.min()),
                                max=int(year.max()),
                                marks={int(y): (y) for y in year.unique()},
                                tooltip={"always_visible": True},
                                step=int(year.unique().sum()),
                                included=False,
                                
                                id='year_slider'), className='year_slider'),

                            # map viewport:
                            html.Div([
                                html.Div([

                                    dl.Map(center=[52.11, 19.21], zoom=6, children=[

                                        dl.TileLayer(),
                                        dl.GeoJSON(id='map_geojson'),
                                        dl.EasyButton(icon='fa-crosshairs', title='Recentre Map', id='btn_recentre'),
                                        dl.Marker(position=[initial_lat, initial_long],
                                                  children=[dl.Tooltip(content=f'Choose year to see the full description')], icon=icon)
                                        
                                    ], className='map', id='map'),
                                    
                                ], className='map_container'),

                                # map options pane:
                                html.Div(
                                    [
                                        html.H1(children='map options:'),
                                        html.Div([html.H1(children='choose map type:'),           
                                                  html.Div([dcc.RadioItems(options=[
                                                      
                                                      {'label': 'Country', 'value': country },
                                                      {'label': 'Voivodeships', 'value': voivodeships },
                                                      {'label': 'Counties', 'value': counties }], 

                                                      value = country, inline=True, id='radio_items')], className='radio')],                      
                                        className='map_type'),

                                        html.Div([html.H1(children='choose region:'),
                                                  html.Div([dcc.Dropdown(sorted([str(coord) for coord in V_COORDS['Voivodeship'].unique() if coord]),
                                                                         maxHeight=150,
                                                                         id='goto_map_reg_dd')], className='region_dropdown')],
                                        className='goto_map_reg'),


                                        html.Div([html.H1(children='filter map by UFO/UAP type:'),
                                                  html.Div([dcc.Dropdown(sorted([str(shape) for shape in DATA['Shape'].unique() if shape]),
                                                                         maxHeight=150,
                                                                         id='filter_map_uaptype_dd')], className='ufo_type_dropdown')],
                                                                          
                                        className='filter_map_uaptype'),

                                    ], className='options_pane')    

                            ])
            ])



## callback functions:

# function for recentering map:
# function for choosing map region:
@app.callback(Output('map', 'viewport'), Input('btn_recentre', 'n_clicks'), Input('goto_map_reg_dd', 'value'))
def recentre_map(center, region):
 
    recentre=[52.11, 19.21]
    zoom = 6

    if region is not None:
        lat = float(V_COORDS[V_COORDS['Voivodeship'] == region]['Lat'])
        long = float(V_COORDS[V_COORDS['Voivodeship'] == region]['Long'])
        recentre = [lat, long]
        zoom = 8
    
    return dict(center=recentre, zoom=zoom, transition = 'flyTo') 



# function for choosing map type:
@app.callback(Output('map_geojson', 'url'), Input('radio_items', 'value'))
def choose_map_type(_):
    
    return _



# function for disabling slider:
@app.callback(Output('year_slider', 'disabled'), Input('filter_map_uaptype_dd', 'value'))
def disable_slider(value):
    if value is not None:

        return True



# function for appending markers:
def append_marker(row, marker_list):

    marker_list.append(dl.Marker(position=[row['Lat'], row['Long']],
                               children=[dl.Tooltip(content=f'Town: {row['Town']}<br>\
                                                              Coords: {row['Lat']}, {row['Long']}<br>\
                                                              Date: {row['Sighted on']}<br>\
                                                              Shape: {row['Shape']}<br>\
                                                              Duration: {row['Duration']}')], icon=icon))



# function for filtering map by year:
# function for filtering map by UFO/UAP type:
@app.callback(Output('map', 'children'), Input('year_slider', 'value'), Input('filter_map_uaptype_dd', 'value'), prevent_initial_call=True)
def choose_year(slider_value, filter_value):

    marker_list = list([dl.TileLayer(),
                        dl.GeoJSON(id='map_geojson'),
                        dl.EasyButton(icon='fa-crosshairs', title='Recentre Map', id='btn_recentre')]
                      )

    for index, row in DATA.iterrows():

        if row['Year'] == slider_value and filter_value is None:
            append_marker(row, marker_list)
            
        elif row['Shape'] == filter_value:
            append_marker(row, marker_list)
        
        else:
            marker_list.append(None)
 
    return marker_list






if __name__ == '__main__':
    app.run_server(debug=False)