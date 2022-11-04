# // {
# //     'a': 0,
# //     'b': [1, 2, 3],
# //     'c': {
# //                 'd': 4,
# //                 'e': 5
# //             },
# //     'g': [{'h': {'a': {'c': 5}, 'b': {'d': 6}}}, {'h': 7}]
#       {'h': {'z': {'c': 5}}
#       {'h': [1, 2, 3, 4, 5]}
# // }
# // ]
# // [
# //   ('a', 0),
# //   ('b', 1),
# //   ('b', 2),
# //   ('b', 3),
# //   ('c.d', 4),
# //   ('c.e', 5),
# //   ('g.h', 6),
# //   ('g.h', 7)
# // ]

# the_dict = values
# result = []
# for key, value in the_dict.items():
#     while not isinstance(value, int):
#         if isinstance(value, dict):
#             for dict_key, dict_value in value:
#                 # result_key = key + "." + dict_key
#                 # result.append((result_key, dict_value))
#         elif isinstance(value, list):
#             for list_val in value:
#                 result.append((key, list_val))
#     # iterate through the length of the value
#         # but have to check data type
#     result.append((key, value))

# // {
# //     'a': 0,
# //     'b': [1, 2, 3],
# //     'c': {
# //                 'd': 4,
# //                 'e': 5
# //             },
# //     'g': [{'h': {'a': {'c': 5}, 'b': {'d': 6}}}, {'h': 7}, {'a': 5}]
#       {'h': {'z': {'c': 5}}
#       {'h': [1, 2, 3, 4, 5]}
# // }
result = []
key = ""
def recurse(key, my_dict):
    # global key

    if isinstance(my_dict, int):
        result.append((key, my_dict))
        # key = ""

    if isinstance(my_dict, dict):
        for dict_key, dict_value in my_dict.items():
            # key = dict_key
            recurse(key + "." + dict_key, dict_value)
        

    if isinstance(my_dict, list):
        for list_val in my_dict:
            recurse(key, list_val)

my_dict = {
    'a': 0,
    'b': [1, 2, 3],
    'c': {
                'd': 4,
                'e': 5
            },
    'g': [{'h': {'a': {'c': 5}, 'b': {'d': 6}}}, {'h': 7}],
    'z': {'h': {'z': {'c': 5}}},
    'y': {'h': [1, 2, 3, 4, 5]}
}

# for key, value in my_dict.items():
#     recurse(key, value)

recurse(key, my_dict)

print(result)