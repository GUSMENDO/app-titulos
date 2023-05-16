import pandas as pd

templates_info = pd.read_csv("data/plantillas_attr.csv")

most_common_attributes = templates_info["att_id"].value_counts()
attributes_to_ignore = most_common_attributes[most_common_attributes==most_common_attributes.max()].index.values.tolist()

names_to_ignore = [" ", "Data", "mirakl", "Mirakl","Reject","reject","Estatus","Evento","Fecha","Descuento","Costo",
                   "Date","Status","Mercancia","Impuesto","IVA"]

for attribute in most_common_attributes.index:
    # print(attribute + ' Atributo a Evaluar')
    for name_to_ignore in names_to_ignore:
        # print(name_to_ignore)
        if name_to_ignore in attribute:
            attributes_to_ignore.append(attribute)

# print(attributes_to_ignore)

templates = {"Ninguna Seleccionada": "Selecciona una plantilla"}

for i, row in templates_info.iterrows():
    if row["att_id"] not in attributes_to_ignore:
        if row["plantilla"] not in templates.keys():
            templates[row["plantilla"]] = []
        templates[row["plantilla"]] += [row["att_id"]]

def get_template_name(template):
    # print(templates_info[templates_info["plantilla"]==template]["nombre_plantilla"].values[0])
    return templates_info[templates_info["plantilla"]==template]["nombre_plantilla"].values[0]


# print(get_template_name('L3-29640359'))