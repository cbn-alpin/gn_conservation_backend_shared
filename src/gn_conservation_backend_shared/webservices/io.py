from uuid import UUID


def prepare_output(d, remove_in_key=None, replace_keys=None):
    if isinstance(d, list):
        new = [] if len(d) > 0 else None
        for item in d:
            output = prepare_output(item, remove_in_key, replace_keys)
            if output:
                new.append(output)
        return new
    elif isinstance(d, dict):
        new = {} if len(d) > 0 else None
        for k, v in d.items():
            # Remove None and empty values
            if v != None and v != "":
                # Replace keys
                if replace_keys and k in replace_keys:
                    k = replace_keys[k]
                # Remove substring in key
                if remove_in_key:
                    new_key = k.replace(remove_in_key, "").strip("_")
                    if new_key != "":
                        k = new_key
                # Value processing recursively
                output = prepare_output(v, remove_in_key, replace_keys)
                if output != None and output != "":
                    new[format_to_camel_case(k)] = output
        return new
    elif isinstance(d, UUID):
        # TODO : implement this in lib "utils_flask_sqla"
        return str(d)
    else:
        return d


def format_to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0].lower() + "".join(x.title() for x in components[1:])


def prepare_input(d):
    if isinstance(d, list):
        output = []
        for item in d:
            output.append(prepare_input(item))
        return output
    elif isinstance(d, dict):
        return dict((format_to_snake_case(k), prepare_input(v)) for k, v in d.items())
    else:
        return d


def format_to_snake_case(camel_str):
    return "".join(["_" + char.lower() if char.isupper() else char for char in camel_str]).lstrip(
        "_"
    )