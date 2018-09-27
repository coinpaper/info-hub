from Validation.Validate import resolve_validation_function, optional


class ValueValidator:

    def __init__(self, yml_value, validation_value, context):
        self.__yml_value = yml_value
        self.__context = context
        self.__validation_functions = []
        self.__validation_arguments = []
        self.resolve_validations(validation_value,)

    def resolve_validations(self, validation_value):
        validations = validation_value.split("|")
        for validation in validations:
            fun, args = resolve_validation_function(validation)
            self.__validation_functions.append(fun)
            self.__validation_arguments.append(args)

    def __is_optional(self):
        return optional in self.__validation_functions

    def validate(self):
        valid = True
        if self.__yml_value is None:
            if self.__is_optional():
                return True
            raise ValueError("Mandatory value is missing in the YML file")
        for (i, func) in enumerate(self.__validation_functions):
            valid = valid and func(
                self.__yml_value,
                argument=self.__validation_arguments[i][0],
                arguments=self.__validation_arguments[i],
                context=self.__context
            )
        return valid
