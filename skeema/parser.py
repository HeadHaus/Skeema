class Parser:
    """
    Parser to build instances of schema
    """
        
    @staticmethod
    def parse_reference(id, id_instance_map):
        if id in id_instance_map:
            return id_instance_map[id]
        raise Exception("Unable to parse reference {}.".format(id))

    @staticmethod
    def parse_instance(cls, lexicon, raw_args):
        # Arguments for the class constructor
        result = []

        # Collect the values for the constructor arguments
        definition = cls.definition
        for parameter_name in definition:
            parameter = definition[parameter_name]
            Type = lexicon.get_type(parameter.type)

            # Get the raw argument 
            if parameter_name in raw_args:
                raw_arg = raw_args[parameter_name]
            else:
                if parameter.required:
                        raise TypeError(f"Argument '{parameter_name}' is required but not supplied.")
                else:
                    if not parameter.array:
                        raw_arg = Type()
                    else:
                        raw_arg = []

            # Standard single value
            if not parameter.array:
                _result = Type.parse(lexicon, raw_arg)
                result.append(_result)
            # Array values
            else:
                _result = []
                for item in raw_arg:
                    _result.append(Type.parse(lexicon, item))
                result.append(_result)

        # Create the new instance
        instance = cls(*result)
        return instance

    # Add parse
    @staticmethod
    def parse(cls, lexicon, raw_args):
        parse_as_reference = False
        if type(raw_args) is str and raw_args[0] == "&":
            parse_as_reference = True

        # if parse_as_reference:
        #     id_start = raw_args.find("&") + 1
        #     id = raw_args[id_start:]
        #     id_instance_map = compilation_context.id_instance_map
        #     instance = Parser.parse_reference(id, id_instance_map)
        # else:


        instance = Parser.parse_instance(cls, lexicon, raw_args)
        return instance
