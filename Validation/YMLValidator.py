from datetime import date
import os

from Validation.Files import validation_yml, open_yml
from Validation.ValueValidator import ValueValidator


class YMLValidator:

    __validation_yml = validation_yml()

    def __init__(self, coin_id):
        self.__yml_to_validate = open_yml(f"./coins/{coin_id}/info.yml")
        self.__coin_id = coin_id

    def validate(self):
        self.validate_structure()
        self.validate_fields()
        self.validate_no_unnecessary_files()
        return True

    def validate_fields(self):
        context = {"coin_id": self.__coin_id}
        path = f"[{self.__coin_id}/info.yml]"
        YMLValidator.__recursive_validation(self.__yml_to_validate, self.__validation_yml, context, path=path)
        return True

    def validate_structure(self):
        path = f"[{self.__coin_id}/info.yml]"
        YMLValidator.__recursive_structure(self.__yml_to_validate, self.__validation_yml, path)
        return True

    def validate_no_unnecessary_files(self, test_images=None, test_files=None):
        ignore_images = test_images if test_images else []
        ignore_files = test_files if test_files else []

        detected_images = os.listdir(os.path.normpath(os.path.join(os.path.dirname(__file__), f"./../coins/{self.__coin_id}/images")))
        detected_files = os.listdir(os.path.normpath(os.path.join(os.path.dirname(__file__), f"./../coins/{self.__coin_id}/files")))

        resolved_images = ignore_images + [self.__yml_to_validate["logo"]] + \
                         [self.__yml_to_validate["team"]["leader"]["imagename"]] + \
                         [member["imagename"] for member in self.__yml_to_validate["team"]["members"]]
        resolved_files = ignore_files + [self.__yml_to_validate["whitepaper"]["file"]]

        for image in detected_images:
            if image not in resolved_images:
                raise ValueError(f"An unecessary image was detected: {self.__coin_id}/images/{image}.")
        for file in detected_files:
            if file not in resolved_files:
                raise ValueError(f"An unecessary file was detected: {self.__coin_id}/images/{file}.")
        return True

    @staticmethod
    def __recursive_structure(value, validation, path):
        if validation is None:
            raise ValueError(f"Illegal Value found in YML: {path}")
        if type(value) == dict:
            if type(validation) != dict:
                raise ValueError(f"Illegal substructure found in YML: {path}")
            for k, v in value.items():
                new_path = f"{path}.{k}"
                if k not in validation.keys():
                    raise ValueError(f"Unecessary key in YML: {new_path}")
                validation_value = validation[k]
                YMLValidator.__recursive_structure(v, validation_value, new_path)
            return
        if type(value) == list and type(validation) == dict:
            for (index, item) in enumerate(value):
                new_path = f"{path}[{index}]"
                YMLValidator.__recursive_structure(item, validation, new_path)
            return
        if type(value) == list and not validation.startswith("foreach"):
            raise ValueError(f"Illegal List found in YML: {path}")

    @staticmethod
    def __recursive_validation(value, validation, context, path):

        # Substructure case
        if type(value) == dict and type(validation) == dict:
            for validation_key, validation_value in validation.items():

                new_path = f"{path}.{validation_key}"

                if validation_key not in value.keys():
                    raise ValueError(f"A key is missing in your YML: {new_path}")

                values_value = value.get(validation_key)

                # Insert opposite into context
                if validation_key == "is_pro":
                    context["opposite"] = value["is_contra"]
                if validation_key == "is_contra":
                    context["opposite"] = value["is_pro"]

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
    v = YMLValidator("usdt-tether")
    v.validate()

