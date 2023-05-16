from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Esta función es para la especificación de los atributos de la regla así como sus nombres
def create_container_rule(idx,
                          template,
                          templates,
                          field_name=None,
                          attribute_name=None,
                          ):
    
    component_id = f'component-{idx}'
    button_remove_id = f'button-remove-{idx}'
    
    dropdown_options = [{'label':'palabra fija','value':'palabra fija'}]
    dropdown_options += [{'label':value, 'value':value} for value in templates[template]]
    # Componente dropdown de selección de atributo
    dropdown = dcc.Dropdown(id={'type':'field-id','index':f'dropdown-{idx}'},
                            placeholder='Atributo o "palabra fija"',
                            options=dropdown_options,
                            value=attribute_name
                            )
    # Componente Input donde el usuario dará nombre al campo
    text_input = dcc.Input(id={'type':'field-name','index':f'text-{component_id}'}, 
                           type='text', 
                           placeholder='Nombre Campo',
                           value=field_name)
    remove_button = html.Button('Remove', 
                                id={'type':'remove-button','id':f'remove-{button_remove_id}'})
    
    container = dbc.Row([
        dbc.Col(text_input,width=5),
        dbc.Col(dropdown,width=5),
        dbc.Col(remove_button,width=2)
        ], id=component_id)
    
    return container

# LA siguiente función servirá para mostrar la regla creada
def generate_html_string(attributes_names,rule_names):
    rule_string = " + ".join(rule_names)
    attribute_string = " + ".join(attributes_names)
    return [
        html.P(rule_string, style={'font-size':'1.2em','text-align':'center'}),
        html.P(attribute_string, className="attribute-name")
    ]

##############################    
## Funciones de excepciones ##
##############################
def create_exception_container(n_clicks,
                               template_attributes,
                               field_names,
                               preselected_attributes_condition=None,
                               preselected_skip_attr=None,
                               preselected_mod_attr=None):
    """Función que regresará los contenedores de excepciones. La lista de preselected_atributes tendrá el siguiente formato: [
                                                                                                                                [
                                                                                                                                    (atributo1,valor_seleccionado1,valor1),
                                                                                                                                    (atributo2,valor_seleccionado2,valor2)],
                                                                                                                                ],
                                                                                                                                [
                                                                                                                                    (atributo3,valor_seleccionado3,valor3),
                                                                                                                                ]
                                                                                                                            ]
        Que se traducirá como: Si (condición1 y condicion2) o condicion3    

    Args:
        n_clicks (_type_): Número de clicks, servirá como index
        template_attributes (list): Lista de atributos preseleccionados
        preselected_attributes_condition (list, optional): Lista de atributos preseleccionados. Defaults to None.

    Returns:
        html.Div: Contenedor deseado
    """
    
    container_condition_id = f'container_condition-{n_clicks}'
    container_modification_id = f'container_modification-{n_clicks}'
    container_id = f'container_exception-{n_clicks}'
     
    # | Si el/los atirbutos... | | Atributo Dropdown| |Condición Dropdown| |Valor (Dropdown incluyendo atributos)| | Y |  |
    #                            | Atributo Dropdown| |Condición Dropdown| |Valor (Dropdown incluyendo atributos)| | Y |  |
    #                                                           |     O      |                                            |
    #                            | Atributo Dropdown| |Condición Dropdown| |Valor (Dropdown incluyendo atributos)| | Y |  | -------> Contenedor "condition"
    container_condition = dbc.Row([
        dbc.Col(
            [html.Div(children=["Si el/los atributo(s):"])],
            width=2
        ),
        ## Contenedor de las condiciones
        dbc.Col(condition_container(template_attributes,
                                    preselected_attributes=preselected_attributes_condition),width=10)])
    
    
    container_modification = dbc.Row([
        dbc.Row([    
                 dbc.Col(html.Div(children=["Entonces:"]),width=2)
                 ], style={'margin-bottom': '30px'}),
        ## Contenedor de las modificaciones
        dbc.Row([
            dbc.Col(html.Div("omitir los campos:"),width=2),
            dbc.Col(html.Div(id=container_modification_id, 
                             children=modification_skip_container(field_names,
                                                                  preselected_skip_attr)),width=10)
        ], style={'margin-bottom': '30px'}),
        html.Br(),
        dbc.Row([
            dbc.Col(html.Div("renombrar los campos:"),width=2),
            dbc.Col(html.Div(id=container_modification_id, 
                             children=modification_rename_container(field_names,
                                                                    preselected_mod_attr)),width=10)
        ], style={'margin-bottom': '40px'}),
        html.Br(),
        dbc.Row([ 
                 dbc.Button("Agregar excepción", id={'type':'add-exception','index':n_clicks})
                 ])
    ])
    
    container_exception = [container_condition,container_modification]
    
    
    return container_exception

## Contenedores de excepciones ##
def condition_container(template_attributes,
                        preselected_attributes,
                        condition_options=None):
    """Contenedor para ingresar una o más condiciones

    Args:
        template_attributes (tuple or list): Tupla o lista con los nombres de los atributos del template
        n_clicks (int): Número de clicks que se han hecho en el botón de agregar excepción
        condition_options (list, optional): Lista con las distintas comparaciones a poner. Defaults to None.
        preselected_attributes (list, optional): Lista con tres elementos: atributo, condición y valor. Defaults to None.
    """
    if condition_options is None:
        condition_options = ['es igual a',
                             'es distinto a',
                             'contiene la(s) palabra(s)',
                             'no contiene la(s) palabra(s)',
                             'es nulo',
                             'no es nulo',
                             'está en',
                             'no está en']
    assert isinstance(condition_options, list), "Las comparaciones deben estar en una lista"
    complete_container = []

    for or_idx,or_element in enumerate(preselected_attributes):
        container = []
        for and_idx, (attribute, comparison, value) in enumerate(or_element):
            attribute_dropdown = dcc.Dropdown(id={'type':f'condition-field-id','index':f'dropdown-{or_idx}-{and_idx}'},
                                    placeholder='Atributo',
                                    options=[{'label':value, 'value':value} for value in template_attributes],
                                    value=attribute
                                    )
            comparison_dropdown = dcc.Dropdown(id={'type':f'condition-field-comparison','index':f'dropdown-{or_idx}-{and_idx}'},
                                            placeholder='Condición',
                                            options=[{'label':value, 'value':value} for value in condition_options],
                                            value=comparison
                                            )
            input_box = dcc.Input(id={'type':f'condition-field-input','index':f'input-box-{or_idx}-{and_idx}'},
                                  type='text',
                                  placeholder='Valor')
            # value_dropdown = dcc.Dropdown(id={'type':f'condition-field-value','index':f'dropdown-{or_idx}-{and_idx}'},
            #                             placeholder='Valor',
            #                             options=[{'label':value, 'value':value} for value in template_attributes],
            #                             multi=False,
            #                             searchable=True,
            #                             value=value
            #                             )
            value_dropdown = dcc.Input(id={'type':f'condition-field-value','index':f'dropdown-{or_idx}-{and_idx}'},
                                       placeholder='Valor',
                                       value=value)
            conditional_and_button = dbc.Button("Y", id={'type':f'condition-field-and','index':f'button-{or_idx}'})
            container.append(
                    dbc.Row([
                        dbc.Col(attribute_dropdown,width=3),
                        dbc.Col(comparison_dropdown,width=3),
                        #dbc.Col(input_box,width=2),
                        dbc.Col(value_dropdown,width=3),
                        dbc.Col(conditional_and_button,width=1),
                        ])
                    )
        conditional_or_button = dbc.Button("O", id={'type' :'condition-field-or','index':f'button-{or_idx}'}, className="button-or")
        container.append(
            dbc.Row(
                    dbc.Col(conditional_or_button,width=8),
                )
            )
        complete_container.append(dbc.Row(container))
    return complete_container
        
def modification_skip_container(template_attributes,
                           preselected_skip_attr):
    """Contenedor para ingresar una o más modificaciones

    Args:
        template_attributes (tuple or list): Tupla o lista con los nombres de los atributos del template
        n_clicks (int): Número de clicks que se han hecho en el botón de agregar excepción
        modification_options (list, optional): Lista con las distintas modificaciones a poner. Defaults to None.
        preselected_skip_attr (list, optional): Lista con dos elementos: atributo y valor. Defaults to None.
    """
    return dcc.Dropdown(id={'type':'modification-skip-id','index':f'dropdown-0'},
                        options=[{'label':value, 'value':value} for value in template_attributes],
                        multi=True,
                        value=preselected_skip_attr)
    
def modification_rename_container(field_names,
                           preselected_mod_attr):
    """Contenedor para ingresar una o más modificaciones

    Args:
        template_attributes (tuple or list): Tupla o lista con los nombres de los atributos del template
        n_clicks (int): Número de clicks que se han hecho en el botón de agregar excepción
        modification_options (list, optional): Lista con las distintas modificaciones a poner. Defaults to None.
        preselected_mod_attr (list, optional): Lista con dos elementos: atributo y valor. Defaults to None.
    """
    container = []
    for idx, (attribute, value) in enumerate(preselected_mod_attr):
        field_name_dropdown = dcc.Dropdown(id={'type':'modification-field-id','index':f'dropdown-{idx}'},
                                placeholder='Atributo',
                                options=[{'label':value, 'value':value} for value in field_names],
                                value=attribute
                                )
        value_input = dcc.Input(id={'type':'modification-field-value','index':f'dropdown-{idx}'},
                                placeholder='Valor',
                                value=value
                                )
        container.append(
                dbc.Row([
                    dbc.Col(html.Div("Cambiar"),width=3),
                    dbc.Col(field_name_dropdown,width=3),
                    dbc.Col(html.Div("por"),width=3),
                    dbc.Col(value_input,width=3),
                    ]),
            )
    return container


def create_example_box():
    """Crea un contenedor para mostrar un ejemplo de cómo se vería la excepción"""
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4("Ejemplo", className="card-title"),
                dbc.Input(id="example-input", placeholder="Escribe los atributos de un producto en formato JSON"),
                dbc.Button("Ver ejemplo", color="primary", id="example-button"),
            ]
        )
    )