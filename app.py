#from dash import Dash, html, dcc, MATCH, ALL
#from dash.dependencies import Input, Output, State
from dash_extensions.enrich import (Output,
                                    DashProxy,
                                    Input,
                                    MultiplexerTransform,
                                    State,
                                    html,
                                    dcc,
                                    ALL,
                                    MATCH)

import dash
import dash_bootstrap_components as dbc
from functions.get_template_info import templates
from functions.components import (create_container_rule,
                                  generate_html_string,
                                  create_exception_container,
                                  )
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from functions.excel_functions import send_title_to_excel

import json

# from assets.styles import (
#     CONTENT_STYLE,
#     OTHER_OPTIONS_STYLE,
#     TEXT_STYLE,
#     NAVBAR_STYLE,
#     DATE_STYLE,
#     TOAST_STYLE,
#     STAR_STYLE,
#     OS_STYLE,
#     BUTTON_STYLE,
#     OTHER_OPTIONS_STYLE,
#     )
    
#For updating requirements.txt: pipreqs path/to/app2.py

app = DashProxy(external_stylesheets=[dbc.themes.BOOTSTRAP],
                transforms=[MultiplexerTransform()],)
#app._favicon = "images/Liverpool.ico"


### NAVBAR ###
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Google Sheets", href="https://docs.google.com/spreadsheets/d/1Ah6QJyzsGe612-VGhiPHiCV5BeLXZQtqzLCewYa2fJE/edit?usp=sharing")),
    ],
    brand="Liverpool creación de títulos",
    brand_href="#",
    color="#CE2C95",
    dark=True,
)

# Define the list of values
values = templates.keys()

# print(values)

### ************* ###
###   First row   ###
### ************* ###

dropdow_menu = dcc.Dropdown(
        id='template-selector',
        placeholder='Selecciona una plantilla',
        options=[{'label': value, 'value': value} for value in values],
        value='Ninguna Seleccionada'
    )
submit_button = dbc.Button('Seleccionar', id='template-button', className="select-template-button")
value_show = html.Div(id='selected-value')
template_name = html.Div(id="template-name")


first_row = dbc.Container(children=dbc.Row([
    dbc.Col(dropdow_menu,width=6),
    dbc.Col(submit_button,width=2),
    dbc.Col(value_show,width=4)]
            )
    )

### ************* ###
###   Second row  ###
### ************* ###
add_component_button = dbc.Button('Añadir campo', id='add-component-button',disabled=True,className="button-add-component")
# This row will ask for the rule creation
second_row = dbc.Container(children = dbc.Row([
    dbc.Col(add_component_button,width=3),
    dbc.Col([dbc.Row([
                dbc.Col(
                    html.Div(children=[""],id="field-name"),
                    width=6),
                dbc.Col(
                    html.Div(children=["Atributo o palabra fija:"],id="field-attribute"),
                    width=6)
                ]),
             html.Div(id='rule-attributes-container', children=[])
             ],
            width=10)
    ])
)



### ************* ###
###   Third row   ###
### ************* ###
third_row = dbc.Container(children=[
    dbc.Row([
        # El botón que permitirá la creación de reglas
        dbc.Col(dbc.Button("Crear excepción",
                           id="add-exception-button",
                           className="button-exception"),
                width=3
                ),
    ]),
    dbc.Row([
        # Aquí irán las excepciones
        dbc.Container(id='container_exceptions', children=[])
        ])
])

### ************* ###
###  Foruth Row    ###
### ************* ###
fourth_row = dbc.Container(children=[
    dbc.Row([
        html.Div(id='created_rules_placeholder', children=["Reglas creadas:"]),
    ]),
    dbc.Row([
        html.Div(id='container_show_created_rules', children=[]),
    ])
])



### ************* ###
###   Fifth row   ###
### ************* ###

### Create rule   ###
create_rule_button = dbc.Button('Crear regla', id='create-rule-button',disabled=True, className="button-create-rule")

# This row will show the created rule
fifth_row = dbc.Container(children=[
    create_rule_button,
    html.Br(),
    dbc.Card(html.Div(id='container_show_created_rule', children=["Regla de la plantilla:"])),
        ],
    id='third-row'
                          )
    



### Sixth Row    ###
sixth_row = dbc.Container(id='example')

#### LAYOUT DE LA APLICACIÓN
app.layout = html.Div([
    dcc.Store(id='rule-att-data', storage_type='memory'),
    dcc.Store(id='rule-exceptions-data', storage_type='memory',data = {'preselected_attributes_condition_0':[[None, None, None]],
                                                                        'preselected_skip_attr':[None],
                                                                        'preselected_mod_attr':[[None,None]],}),
    dbc.Container([
        navbar,
        html.Br(),
        first_row,
        html.Hr(),
        second_row,
        html.Br(),
        third_row,
        html.Hr(),
        fourth_row,
        html.Hr(),
        fifth_row,
        html.Hr(),
        sixth_row
    ])
])
#### FIRST ROW
# Plantilla seleccionada callback
@app.callback(
    dash.dependencies.Output('selected-value', 'children'),
    [dash.dependencies.Input('template-button', 'n_clicks')],
    [dash.dependencies.State('template-selector', 'value')]
)
def update_selected_value(n_clicks, selected_value):
    return f'Plantilla seleccionada: {selected_value}'


#### SECOND ROW
#Añadir campo de regla callback: AÑADIR CAMPO
@app.callback(Output('rule-attributes-container', 'children'),
              [Input('add-component-button', 'n_clicks')],
              [State('template-selector', 'value'),
               State('rule-att-data', 'data')])
               
def add_component(n_clicks,template, data):
    if n_clicks is None:
        return []
    else:
        field_names = data['field_names']
        attribute_names = data['attribute_names']
        containers = []
        for idx,(field_name,attribute_name) in enumerate(zip(field_names,attribute_names)):
            container = create_container_rule(idx,
                                            template,
                                            templates,
                                            field_name,
                                            attribute_name)
            containers.append(container)
        return containers + [create_container_rule(n_clicks,template,templates)]
# Mostrar botón de AÑADIR regla: AÑADIR CAMPO VISIBLE
@app.callback(Output('add-component-button', 'disabled'),
              [Input('template-button', 'n_clicks')])
def enable_add_component_button(n_clicks):
    if n_clicks is None:
        return True
    else:
        return False
# Actualizar storage de la sesión
@app.callback(Output('rule-att-data', 'data'),
              [Input({'type':'field-id','index':ALL},"value"),
               Input({'type':'field-name','index':ALL},"value")],
              prevent_initial_call=False
              )
def update_rule_att_data(attribute_names,field_names):
    attributes_list = []
    field_list = []
    
    for attribute,field in zip(attribute_names,field_names):
        if attribute is None:
            attributes_list.append(attribute)
            field_list.append(field)
        elif attribute.lower() == "palabra fija":
            attributes_list.append(f'"{field}"')
            field_list.append(field)
        else:
            attributes_list.append(attribute)
            field_list.append(field)
    updated_data = {'field_names':field_list,
                    'attribute_names':attributes_list}
    
    return updated_data    


#### third ROW
# Mostar botón de CREAR regla: CREAR REGLA
@app.callback(Output('create-rule-button', 'disabled'),
              [Input('add-component-button', 'n_clicks')])
def enable_create_rule_button(n_clicks):
    if n_clicks is None:
        return True
    else:
        return False
# Mostrar la regla creada
@app.callback(Output('container_show_created_rule', 'children'),
                [Input('create-rule-button', 'n_clicks')],
                [State({'type':'field-id','index':ALL},"value"),
                 State({'type':'field-name','index':ALL},"value"),
                 State('template-selector','value'),
                 State('rule-att-data', 'data')],
                prevent_initial_call=True)
def show_created_rule(n_clicks,field_id,field_name,template_name,rule_att_data):
    html_string = dcc.Markdown(f'Regla de la plantilla: **{template_name}**')
    
    #html_rule_string1, html_rule_string2 = generate_html_string(field_id,field_name)
    html_rule_string1, html_rule_string2 = generate_html_string(rule_att_data["attribute_names"],
                                                                rule_att_data["field_names"])
    if n_clicks is not None:
        to_excel_button = dbc.Row(dbc.Button(
            "Copiar en Excel", 
            id={'type':'excel_button','id':"copy-button"}, 
            color="primary", 
            className="button-excel",
            ),justify="center")
        return dbc.Container([html_string,html_rule_string1, html_rule_string2,to_excel_button])
    else:
        return dbc.Container([html_string,html_rule_string1, html_rule_string2],class_name="rule-container")
# Button to copy in excel
@app.callback(Output('third-row', 'children'),
              Input({'type':'excel_button','id':ALL}, 'n_clicks'),
              [State({'type':'field-id','index':ALL},"value"),
               State({'type':'field-name','index':ALL},"value"),
               State('template-selector','value'),
               State('third-row', "children")])
def title_to_excel(n_clicks,attributes_names,rule_names,template_name,existing_children):
    if not len(n_clicks):
        return existing_children
    elif n_clicks[0] is None:
        return existing_children
    rule_string = " + ".join(rule_names)
    attribute_string = " + ".join(attributes_names)
    
    if send_title_to_excel(rule_string,attribute_string,template_name,):
        return existing_children + [html.P('Copiado en excel')]
    else:
        return existing_children + [html.P('Error. No copiado en excel')]

#### fourth ROW
@app.callback([Output('container_exceptions', 'children')],
              [Input('add-exception-button', 'n_clicks'),
               Input('rule-att-data', 'data'),
               Input('rule-exceptions-data','data')],
              prevent_initial_call=False)
def add_exception(n_clicks,
                  attr_data,
                  rule_exceptions_data):
    if n_clicks is None:
        return []
    else:
        field_names = attr_data['field_names']
        attribute_names = attr_data['attribute_names']
        preselected_attributes_condition = [ condition 
                                            for key,condition in rule_exceptions_data.items()
                                            if key.startswith('preselected_attributes_condition_')
                                            ]
        preselected_skip_attr = rule_exceptions_data['preselected_skip_attr']
        preselected_mod_attr = rule_exceptions_data['preselected_mod_attr']
        container = create_exception_container(n_clicks,
                                               attribute_names,
                                               field_names,
                                               preselected_attributes_condition,
                                               preselected_skip_attr,
                                               preselected_mod_attr)
        return container
#Inicializar storage de la sesión

# Cambiar dinámicamente las condiciones
@app.callback(Output('rule-exceptions-data', 'data'),
            [Input({'type':f'condition-field-id','index':ALL},"value"),
            Input({'type':f'condition-field-comparison','index':ALL},"value"),
            Input({'type':f'condition-field-value','index':ALL},"value"),],
            [State('rule-exceptions-data', 'data'),
            #State({'type':f'condition-field-id-{idx_or}','index':ALL},'id')
            ],
            prevent_initial_call=True)
def update_conditions_data(condition_attr,
                            condition_comparison,
                            condition_value,
                            rule_exceptions_data,
                            #condition_id
                            ):
    ctx = dash.callback_context
    triggered = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    _, idx_or, idx_and = triggered['index'].split('-')
    value = ctx.triggered[0]['value']
    idx_and = int(idx_and)
    index_update = f'preselected_attributes_condition_{idx_or}'
    condition_to_update = rule_exceptions_data[index_update]
    
    print("Componente modificado: ",ctx.triggered)
    print("Before update:",condition_to_update)
    
    if triggered['type'] == 'condition-field-id':
        print(condition_attr)
        condition_to_update[idx_and][0] = value
    
    elif triggered['type'] == 'condition-field-comparison':
        condition_to_update[idx_and][1] = value
        
    elif triggered['type'] == 'condition-field-value':
        condition_to_update[idx_and][2] = value
    else:
        print("No se ha modificado nada")
        print(f"Triggered: {triggered}")
    
    print("After update:",condition_to_update)
    rule_exceptions_data[index_update] = condition_to_update
    print(rule_exceptions_data)
    return rule_exceptions_data
    
# Cambiar dinámicamente las modificaciones
@app.callback(Output('rule-exceptions-data', 'data'),
              [Input({'type':'modification-skip-id','index':ALL},"value"),
               Input({'type':'modification-field-id','index':ALL},"value"),
               Input({'type':'modification-field-value','index':ALL},"value")],
              State('rule-exceptions-data', 'data'),
              prevent_initial_call=True)
def update_rule_exceptions_data(skip_attr,
                                mod_attr_attr,
                                mod_attr_value,
                                rule_exceptions_data):
    modification = list(zip(mod_attr_attr,mod_attr_value))
    rule_exceptions_data['preselected_skip_attr'] = skip_attr[0]
    rule_exceptions_data['preselected_mod_attr'] = modification    
    return rule_exceptions_data

# Hacer funcionar los botones AND
@app.callback(Output('rule-exceptions-data', 'data'),
            Input({'type':f'condition-field-and','index':ALL},"n_clicks"),
            State('rule-exceptions-data', 'data'),
            prevent_initial_call=True)
def add_fields_and(n_clicks,rule_exceptions_data):
    if not n_clicks:
        return rule_exceptions_data
    ctx = dash.callback_context
    triggered = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
    _, or_idx = triggered['index'].split('-')
    
    to_modify = f'preselected_attributes_condition_{or_idx}'
    rule_exceptions_data[to_modify] = rule_exceptions_data[to_modify] + [[None, None, None]]
    return rule_exceptions_data

# Hacer funcionar los botones OR
@app.callback(Output('rule-exceptions-data', 'data'),
            Input({'type':f'condition-field-or','index':ALL},"n_clicks"),
            State('rule-exceptions-data', 'data'),
            prevent_initial_call=True)
def add_fields_or(n_clicks,rule_exceptions_data):
    if not n_clicks:
        return rule_exceptions_data
    conditions_list = [key for key in rule_exceptions_data.keys() if 'preselected_attributes_condition' in key]
    conditions_list.sort()
    new_key = f'preselected_attributes_condition_{len(conditions_list)}'
    rule_exceptions_data[new_key] = [[None, None, None]]
    return rule_exceptions_data
    
#### FIFTH ROW
@app.callback([Output('container_show_created_rules', 'children'),
               Output('rule-exceptions-data', 'data')],
              Input({'type':'add-exception','index':ALL}, 'n_clicks'),
              [State('rule-exceptions-data', 'data'),
               State('container_show_created_rules', 'children')],
              prevent_initial_call=True)
def show_created_rules(n_clicks,
                       rule_exceptions_data,
                       previous_rules):
    if not n_clicks or n_clicks == [None]:
        return previous_rules, rule_exceptions_data
    new_rules = {'preselected_attributes_condition_0':[[None, None, None]],
                'preselected_skip_attr':[None],
                'preselected_mod_attr':[[None,None]],}
    try:
        ## Condicionales
        conditionals_keys = [key for key in rule_exceptions_data.keys() if 'preselected_attributes_condition' in key]
        conditional_string = "SI "
        conditionals_string_list = []
        for i in range(len(conditionals_keys)):
            aux_string = "("
            conditionals = rule_exceptions_data[conditionals_keys[i]]
            print(conditionals)
            result = [" ".join(sublist) for sublist in conditionals]
            final_result = " Y ".join(result)
            aux_string += final_result
            aux_string += ")"
            conditionals_string_list.append(aux_string)
        conditional_string += " O ".join(conditionals_string_list)
        
        final_string = conditional_string
        
        final_string+= " ENTONCES "
        if rule_exceptions_data['preselected_skip_attr'] != [None]:
            final_string+=" OMITIR "
            final_string+= ",".join(rule_exceptions_data['preselected_skip_attr'])
        
        if rule_exceptions_data['preselected_mod_attr'] !=  [[None, None]]:
            final_string+=" CAMBIAR "
            result = [" por ".join(sublist) for sublist in rule_exceptions_data['preselected_mod_attr']]
            final_result = " Y ".join(result)
            final_string+= final_result
        
        if  previous_rules == []:
            return final_string, new_rules
        else:
            previous_rules_strings = previous_rules.split("\n")
            previous_rules_strings.append(final_string)
            return "\n".join(previous_rules_strings), new_rules
    except:
        return previous_rules, rule_exceptions_data        
 
 ### SIXTH ROW
#  @app.callback(Output('example','children'),
#                Input({'type':'add-exception','index':ALL}, 'n_clicks'),
#                State('rule-exceptions-data', 'data'),
#                State('container_show_created_rules', 'children'))

#### DESHABILITACIONES
# Deshabilitar botones dropdown: DESHABILITAR ATRIBUTOS SELECT
@app.callback(Output({'type':'field-id','index':MATCH},"disabled",),
[Input('create-rule-button', 'n_clicks')])
def set_field_id_readonly(n_clicks):
    if n_clicks is None:
        return False
    else:
        return True
# Deshabilitar botones inputs: DESHABILITAR INPUT NOMBRE DEL CAMPO
@app.callback(Output({'type':'field-name','index':MATCH},"disabled",),
              Input('create-rule-button', 'n_clicks'))
def set_field_name_readonly(n_clicks):
    if n_clicks is None:
        return False
    else:
        return True
# Deshabilitar botones de quitar reglas: DESHABILITAR BOTÓN REMOVER
@app.callback(Output({'type':'remove-button','index':MATCH},"disabled",),
              Input('create-rule-button', 'n_clicks'))
def set_remove_button_disabled(n_clicks):
    if n_clicks is None:
        return False
    else:
        return True
#Deshabilitar crear excepcion button
@app.callback(Output('add-exception-button', 'disabled'),
              [Input('create-rule-button', 'n_clicks')])
def enable_add_exception_button(n_clicks):
    if n_clicks is None:
        return True
    else:
        return False
    

### CALLBACKS PARA ELIMINAR/AGREGAR children
# Show field "Nombre del campo" text
@app.callback(Output('field-name','children'),
              Input('add-component-button', 'n_clicks'),)
def show_field_name_text(n_clicks):
    if n_clicks is None:
        return []
    else:
        return [html.P('Nombre del campo:')]
# Show field "Nombre del atributo o palabra fija" text
@app.callback(Output('field-attribute','children'),
              Input('add-component-button', 'n_clicks'),)
def show_field_attribute_text(n_clicks):
    if n_clicks is None:
        return []
    else:
        return [html.P('Nombre del atributo o palabra fija:')]



if __name__ == '__main__':
    app.run_server(debug=True)