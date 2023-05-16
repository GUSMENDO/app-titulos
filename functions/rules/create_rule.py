
class rule:
    def __init__(self, template, structure, exceptions=None):
        self.template = template
        assert isinstance(structure, list)
        self.structure = structure
        self.attributes_used = [ attribute for field, attribute in structure]
        self.exceptions = exceptions
    
    def make_title_from_attributes(self,attributes):
        title = ""
        assert isinstance(attributes, dict)
        assert set(self.attributes_used) <= set(attributes.keys())
        for field_name,atrribute in self.structure:
            