import gspread
from google.auth import load_credentials_from_file
import logging


class excel_doc_class():
    def __init__(self) -> None:
        self.gc = None
        self. creds = None
        self.worksheet = None
        self.has_already_authenticate = False

excel_doc = excel_doc_class()

def intialize(excel_doc=excel_doc):
    """Función que inicializará las configuraciones necesarias de excel para conectarse
    con la API, esto logrará que solo se conecte una vez y ya no repita el proceso cada
    vez que se quiera escribir algo en excel

    Args:
        excel_doc (excel_doc_class, optional): Objeto de la clase excel_doc que se irá escribiendo. Defaults to excel_doc.
    """
    scope = ['https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive"]

    excel_doc.creds = load_credentials_from_file("keys/credentials.json",scopes=scope)[0]
    excel_doc.gc = gspread.authorize(excel_doc.creds)
    excel_doc.has_already_authenticate = True
    
    url = "https://docs.google.com/spreadsheets/d/1Ah6QJyzsGe612-VGhiPHiCV5BeLXZQtqzLCewYa2fJE/edit?usp=sharing"
    excel_doc.worksheet = excel_doc.gc.open_by_url(url).worksheet("Reglas de Títulos PRUEBAS")
    
def send_title_to_excel(title_name,title_atts,template,excel_doc=excel_doc):
    if not excel_doc.has_already_authenticate:
        intialize(excel_doc)
    
    cell_value = title_name+"\n"+title_atts
    
    try:
        excel_doc.worksheet.append_row([template,cell_value],1)
        logging.info(f"Excel has been modified: Appended template: {template}")
        return True
    except Exception as e:
        logging.warning(f"Error {e}: Excel has not been modified")
        return False
    
    