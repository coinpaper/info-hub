from datetime import date
import os

from Validation.Files import validation_yml, open_yml
from Validation.ValueValidator import ValueValidator

EMPTY_FILE = ".empty"

class YMLValidator:

    __validation_yml = validation_yml()

    def __init__(self, coin_id):
        self.__yml_to_validate = open_yml(f"./coins/{coin_id}/info.yml")
        self.__coin_id = coin_id
        self.structure_errors = []
        self.field_errors = []
        self.file_errors = []

    def validate(self):
        self.validate_structure()
        self.validate_fields()
        self.validate_no_unnecessary_files()
        if len(self.structure_errors + self.field_errors + self.file_errors) == 0:
            return True
        error_str = "\n"
        error_types = {
            "Structure Errors": self.structure_errors,
            "Field Errors": self.field_errors,
            "File Errors": self.file_errors,
        }
        for error_name, error_list in error_types.items():
            if len(error_list) > 0:
                error_str += f"*** {error_name} ***\n"
                for error in error_list:
                    error_str += f"- {error}\n"
        raise ValueError(error_str)

    def validate_fields(self):
        context = {"coin_id": self.__coin_id}
        path = f"[{self.__coin_id}/info.yml]"
        self.__recursive_validation(self.__yml_to_validate, self.__validation_yml, context, path=path)
        return True

    def validate_structure(self):
        path = f"[{self.__coin_id}/info.yml]"
        self.__recursive_structure(self.__yml_to_validate, self.__validation_yml, path)
        return True

    def validate_no_unnecessary_files(self, test_images=None, test_files=None):
        ignore_images = test_images if test_images else []
        ignore_files = test_files if test_files else []

        detected_images = os.listdir(os.path.normpath(os.path.join(os.path.dirname(__file__), f"./../coins/{self.__coin_id}/images")))
        detected_files = os.listdir(os.path.normpath(os.path.join(os.path.dirname(__file__), f"./../coins/{self.__coin_id}/files")))

        detected_images = list(filter(lambda d: d != EMPTY_FILE, detected_images))
        detected_files = list(filter(lambda d: d != EMPTY_FILE, detected_files))

        leader_image = []
        if self.__yml_to_validate["team"]["leader"]:
            leader_image = [self.__yml_to_validate["team"]["leader"]["imagename"]]
        resolved_images = ignore_images + [self.__yml_to_validate["logo"]] + \
                         leader_image + \
                         [member["imagename"] for member in self.__yml_to_validate["team"]["members"]]
        resolved_files = ignore_files + [self.__yml_to_validate["whitepaper"]["file"]]

        for image in detected_images:
            if image not in resolved_images:
                self.file_errors.append(f"An unecessary image was detected: {self.__coin_id}/images/{image}.")
        for file in detected_files:
            if file not in resolved_files:
                self.file_errors.append(f"An unecessary file was detected: {self.__coin_id}/images/{file}.")
        return True

    def __recursive_structure(self, value, validation, path):
        if validation is None:
            self.structure_errors.append(f"Illegal Value found in YML: {path}")
        if type(value) == dict:
            if type(validation) != dict:
                self.structure_errors.append(f"Illegal substructure found in YML: {path}")
            for k, v in value.items():
                new_path = f"{path}.{k}"
                if k not in validation.keys():
                    self.structure_errors.append(f"Unecessary key in YML: {new_path}")
                validation_value = validation[k]
                self.__recursive_structure(v, validation_value, new_path)
            return
        if type(value) == list and type(validation) == dict:
            for (index, item) in enumerate(value):
                new_path = f"{path}[{index}]"
                self.__recursive_structure(item, validation, new_path)
            return
        if type(value) == list and not validation.startswith("foreach"):
            self.structure_errors.append(f"Illegal List found in YML: {path}")

    def __recursive_validation(self, value, validation, context, path):

        # Substructure case
        if type(value) == dict and type(validation) == dict:
            for validation_key, validation_value in validation.items():

                new_path = f"{path}.{validation_key}"

                if validation_key not in value.keys():
                    self.field_errors.append(f"A key is missing in your YML: {new_path}")

                values_value = value.get(validation_key)

                # Insert opposite into context
                if validation_key == "is_pro":
                    context["opposite"] = value["is_contra"]
                if validation_key == "is_contra":
                    context["opposite"] = value["is_pro"]

                self.__recursive_validation(values_value, validation_value, context, path=new_path)
            return

        if type(value) == list and type(validation) == dict:
            for (index, item) in enumerate(value):
                new_path = f"{path}[{index}]"
                self.__recursive_validation(item, validation, context, new_path)
            return

        if (type(value) in [list, int, float, str, bool] or isinstance(value, date) or value is None) and type(validation) == str:
            validator = ValueValidator(value, validation, context)
            try:
                validator.validate()
            except ValueError as e:
                self.field_errors.append(f"YML validation error at path '{path}': {str(e)}")
            return

        self.field_errors.append(f"YML parsing error: value='{value}', validation='{validation}'")


if __name__ == "__main__":
    v = YMLValidator("dot-polkadot")
    v.validate()

