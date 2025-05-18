from abc import ABC, abstractmethod

class FieldInterface(ABC):
    @property
    @abstractmethod
    def tag(self) -> str:
        pass

    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @property
    @abstractmethod
    def attributes(self) -> dict:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def options(self) -> list:
        pass

class Field(FieldInterface):
    def __init__(self, field_data: dict):
        for prop in field_data:
            if not hasattr(self, prop):
                raise ValueError(f"Invalid property {prop} on Field instance")
            setattr(self, prop, field_data[prop])
        self._validate()

    def _validate(self):
        interface = FieldInterface.__dict__
        for prop in interface:
            if not hasattr(self, prop) and callable(getattr(FieldInterface, prop)):
                raise ValueError(f"{prop} is required on Field instance")

class FormGenerator:
    def __init__(self):
        self.field_count = 0
        self.form_container = []

    def add_field(self, field_data: dict) -> None:
        field = Field(field_data)
        element = {}
        tag = field.tag or field.type
        if tag in ['span', 'select', 'textarea', 'label', 'input', 'radio', 'checkbox']:
            element['tag'] = tag
            for attr, value in field.attributes.items():
                element[attr] = value
            if tag == 'span':
                element['text'] = field.text
            elif tag == 'select':
                element['options'] = [{'value': opt.get('attributes', {}).get('value'), 'text': opt.get('attributes', {}).get('text')} for opt in field.options]
        else:
            raise ValueError(f"Unsupported tag {tag}")

        if not element.get('name'):
            element['name'] = f'field{self.field_count}'
            self.field_count += 1

        self.form_container.append(element)
