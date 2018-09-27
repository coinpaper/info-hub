from datetime import date

from Validation.Files import validation_yml, open_yml
from Validation.ValueValidator import ValueValidator


class YMLValidator:

    __validation_yml = validation_yml()

    def __init__(self, coin_id):
        self.__yml_to_validate = open_yml(f"./coins/{coin_id}/info.yml")
        self.__coin_id = coin_id

    def validate(self):
        self.__validate_structure()
        self.__validate_fields()
        self.__validate_no_unnecessary_files()
        return True

    def __validate_fields(self):
        context = {"coin_id": self.__coin_id}
        path = f"[{self.__coin_id}/info.yml]"
        YMLValidator.__recursive_validation(self.__yml_to_validate, self.__validation_yml, context, path=path)
        return True

    def __validate_structure(self):
        pass

    def __validate_no_unnecessary_files(self):
        pass

    @staticmethod
    def __recursive_validation(value, validation, context, path):

        # Substructure case
        if type(value) == dict and type(validation) == dict:
            for validation_key, validation_value in validation.items():

                if validation_key not in value.keys():
                    raise ValueError(f"A key is missing in your YML: {validation_key}")

                values_value = value.get(validation_key)

                # Insert opposite into context
                if validation_key == "is_pro":
                    context["opposite"] = value["is_contra"]
                if validation_key == "is_contra":
                    context["opposite"] = value["is_pro"]

                new_path = f"{path}.{validation_key}"
                YMLValidator.__recursive_validation(values_value, validation_value, context, path=new_path)
            return

        if type(value) == list and type(validation) == dict:
            for (index, item) in enumerate(value):
                new_path = f"{path}[{index}]"
                YMLValidator.__recursive_validation(item, validation, context, new_path)
            return

        if (type(value) in [list, int, float, str, bool] or isinstance(value, date) or value is None) and type(validation) == str:
            validator = ValueValidator(value, validation, context)
            try:
                validator.validate()
            except ValueError as e:
                raise ValueError(f"YML validation error at path '{path}': {str(e)}")
            return

        raise ValueError(f"YML parsing error: value='{value}', validation='{validation}'")


if __name__ == "__main__":
    v = YMLValidator("test-testing-coin")
    v.validate()

