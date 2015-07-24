from data.vehicle_type_data import VEHICLE_TYPE_DICT

def get_vehicle_type_details(type_list):
    for type in type_list:
        if type.name in VEHICLE_TYPE_DICT:
            type.attrs = VEHICLE_TYPE_DICT[type.name]
            print type
    return type_list