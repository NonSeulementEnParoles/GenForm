<?php

interface FieldInterface {
    public function getTag(): string;
    public function getType(): string;
    public function getAttributes(): array;
    public function getText(): string;
    public function getOptions(): array;
}

class Field implements FieldInterface {
    private $tag, $type, $attributes, $text, $options;

    public function __construct(array $field_data) {
        foreach ($field_data as $prop => $value) {
            if (!property_exists($this, $prop)) {
                throw new Exception("Invalid property {$prop} on Field instance");
            } else {
                $this->{$prop} = $value;
            }
        }
        $this->_validate();
    }

    private function _validate(): void {
        foreach (get_class_vars(FieldInterface::class) as $prop => $value) {
            if (!property_exists($this, $prop)) {
                throw new Exception("{$prop} is required on Field instance");
            }
        }
    }

    public function getTag(): string {
        return $this->tag;
    }

    // And so on for other methods...
}

class FormGenerator {
    private $field_count = 0;
    private $form_container = [];

    public function addField(array $field_data): void {
        $field = new Field($field_data);
        $element = [];
        $tag = $field->getTag() ?? $field->getType();
        if (in_array($tag, ['span', 'select', 'textarea', 'label', 'input', 'radio', 'checkbox'])) {
            $element['tag'] = $tag;
            foreach ($field->getAttributes() as $attr => $value) {
                $element[$attr] = $value;
            }
            // And so on for other conditions...
        } else {
            throw new Exception("Unsupported tag {$tag}");
        }
    }

    // And so on for other methods...
}

?>
