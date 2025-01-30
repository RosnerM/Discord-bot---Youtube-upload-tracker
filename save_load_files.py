import json
from datetime import datetime
import os



#------------------------------Savers
def save_dict_to_file(dictionary, filename):
    """Save a dict to json. Also accepts list or str"""

    def default_serializer(obj): 
        """allows saving datetime data to json (else cannot save to json)"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            raise TypeError("Object of type %s is not JSON serializable" % type(obj))

    with open(filename, 'w') as file:
        json.dump(dictionary, file, default=default_serializer)






#------------------------Loaders


#1) Int keys dictionary loader
def load_int_dict_from_file(filename):
    with open(filename, 'r') as file:
        loaded_dict = json.load(file)
        # Convert keys back to integers if they were originally integers
        return {int(key): value for key, value in loaded_dict.items()}





#2) (default in Python) Str keys dictionary loader
def load_dict_lst_or_str__from_jsonfile(filename):
    def decode_datetime(obj):
        """
        Function to convert datetime strings to datetime objects during JSON decoding.
        """
        for key, value in obj.items():
            if isinstance(value, str):
                try:
                    print(f'Trying to load datetime value: {value}')
                    obj[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    print('Success...')
                except ValueError:
                    print(f'Error, could not load value: {value} as a datetime obj')
                    pass  # Handle if the value is not a valid datetime string
        return obj
    with open(filename, 'r') as file:
        loaded_data = json.load(file, object_hook=decode_datetime)
        return loaded_data
    



#-------------------------Advanced Loader
def load_var_from_json(data, filename, keys='str'):
    """I.e. load_var_from_json(data=roles_dict_var, filename='CAT.json', key='int')
    Keys can be str on int for the loaded dict."""

    if os.path.exists(filename):
        print(f'>{filename} json exists, loading...')
        if keys=='int':
            return load_int_dict_from_file(filename) #dict with int keys
        else:
            return load_dict_lst_or_str__from_jsonfile(filename) #dict with str keys
    else:
        print(f'>No json file detected of {filename}. Loading already set defaults...')
        save_dict_to_file(data, filename) #save the defaults to json, just so that the json file is created already
        return data #dict, str, or list