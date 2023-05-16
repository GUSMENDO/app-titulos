import re

class rule():
    def __init__(self, field_names, attribute_names, rules):
        self.field_names = field_names
        self.attribute_names = attribute_names
        self.rules = rules
        self.condition_options = ['es igual a',
                                'es distinto a',
                                'no contiene la(s) palabra(s)',
                                'contiene la(s) palabra(s)',
                                'no es nulo',
                                'es nulo',
                                'está en',
                                'no está en']
        self.base_rules()
    
    def base_rules(self):
        if not self.rules:
            self.rules 
        # Rules será una string con el formato SI (...) O (...)... ENTONCES OMITIR ... CAMBIAR (...)
        pattern = r"SI\s+(.*?)ENTONCES"
        match = re.search(pattern, self.rules)
        if match:
            conditionals = match.group(1).split("O")
        else:
            raise Exception("No se encontró la condición SI (...) ENTONCES")
        conditionals_list = []
        for conditional in conditionals:
            conditionals_aux_list = []
            conditional = conditional.strip().replace("(", "").replace(")", "")
            conditional_sublist = conditional.split("Y")
            for condition in conditional_sublist:
                condition = condition.strip()
                attribute, comparison, value = None, None, None
                for comparison_string in self.condition_options:
                    if comparison_string in condition:
                        attribute, value = condition.split(comparison_string)
                        comparison = comparison_string
                        break
                assert isinstance(value,str) and isinstance(attribute,str)
                conditionals_aux_list.append([attribute.strip(), comparison, value.strip()])
            conditionals_list.append(conditionals_aux_list)
        self.conditionals_list = conditionals_list
        
        # Sabemos que después de ENTONCES viene OMITIR o CAMBIAR o los dos, pero siempre en ese orden
        # Caso 1 solo está omitir
        if "OMITIR" in self.rules and "CAMBIAR" not in self.rules:
            skip_attributes = self.rules.split("OMITIR")[1].split(",")
            self.skip_list = [attribute.strip() for attribute in skip_attributes]
        # Caso 2 solo está cambiar
        if "CAMBIAR" in self.rules and "OMITIR" not in self.rules:
            change_attributes = self.rules.split("CAMBIAR")[1].split("Y")
            change_list = []
            for change_attribute in change_attributes:
                attribute,value = change_attribute.split("POR")
                change_list.append([attribute.strip(), value.strip()])
            self.change_list = change_list
        # CASO 3
        if "CAMBIAR" in self.rules and "OMITIR" in self.rules:
            skip_attributes = self.rules.split("OMITIR")[1].split("CAMBIAR")[0].split(",")
            self.skip_list = [attribute.strip() for attribute in skip_attributes]
            
            change_attributes = self.rules.split("CAMBIAR")[1].split("Y")
            change_list = []
            for change_attribute in change_attributes:
                attribute,value = change_attribute.split("POR")
                change_list.append([attribute.strip(), value.strip()])
            self.change_list = change_list
        
        return 
                
            
            
    
    def convert_attribute_to_title(self, attributes_dict):
        pass