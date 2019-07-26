from unittest.mock import Mock, MagicMock


mocked_dogs_attrs = {"name.return_value": "https://dog.ceo/api/breeds/list/all", "get_responce_code.return_value": 200,
                     "elements_count.return_value": 100, "get_responce_status_by_entry.return_value": 200,
                     "get_total_breeds_count.return_value": 2, "count_images_by_breed.return_value":
                         {"Yorkshire terrier": 23, "Baskerville chihuahua": 1}}

mocked_brew_attrs = {"name.return_value": "https://api.openbrewerydb.org/breweries",
                     "get_responce_code.return_value": 200, "elements_count.return_value": 20,
                     "get_count_by_state.return_value": {"new_york": 15, "california": 20, "arizona": 75,
                                                         "alabama": 39, "ohio": 55},
                     "get_responce_status_by_endings.return_value": 200,
                     "search_animals.return_value": {"dog": 123, "cat": 764, "fish": 65},
                     "get_id_by_name.return_value": {"dog":
                                                         ['530', '542', '1221', '2268', '3025', '3068', '3136', '4121',
                                                          '4263', '4555', '5359', '5925', '7152', '7424', '7704'],
                                                     "cooper":
                                                         ['58', '3208', '6998', '7900', '3809', '3827', '4674', '5773',
                                                          '6393', '6600', '7465', '3828', '2185', '4638', '4679'],
                                                     "sisters": ['5961', '5960', '6930', '7715', '281', '6643']
                                                     }
                     }

mocked_cdnjs_attrs = {"name.return_value": "https://api.cdnjs.com/libraries", "get_responce_code.return_value": 200,
                      "get_responce_code_by_entry.return_value": 200, "elements_count.return_value": 40,
                      "search_by_text.return_value": {"bootstrap": 185, "alert": 25},
                      "match_number_by_field.return_value": {"version": 20, "description": 20, "homepage": 20,
                                                             "keywords": 20, "license": 20,
                                                             "repository": 20, "autoupdate": 20, "author": 20,
                                                             "assets": 20}
                      }

mocked_dogs = Mock(**mocked_dogs_attrs)
mocked_brew = Mock(**mocked_brew_attrs)
mocked_cdnjs = Mock(**mocked_cdnjs_attrs)
