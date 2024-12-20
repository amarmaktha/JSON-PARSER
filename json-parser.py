import json
from decimal import Decimal
# Here I am using recursion to parse the data fron json string to list or objects.
def parse_json_to_list(json_string):
    def custom_decoder(obj):
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    if '.' in value or 'e' in value.lower():
                        obj[key] = Decimal(value)
                except Exception:
                    pass 
        return obj

    def flatten_to_list(data):
        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                result.extend(flatten_to_list(value))
            return result
        elif isinstance(data, list):
            result = []
            for item in data:
                result.extend(flatten_to_list(item))
            return result
        else:
            return [data]

    try:
        parsed_data = json.loads(
            json_string,
            parse_float=Decimal,
            parse_int=int,
            object_hook=custom_decoder
        )
        return flatten_to_list(parsed_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string: {e}")


# Example Usage
json_string = '{"integer": 123456789123456789123456789, "float": 1.23456789123456789, "list": [1, 2, "text"], "nested": {"key": "1.2345678901234567890"}}'

parsed_list = parse_json_to_list(json_string)
print(type(parsed_list))
print(parsed_list)
