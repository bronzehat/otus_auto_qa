from unittest.mock import Mock, MagicMock


mocked_dogs = Mock()
mocked_dogs.name = MagicMock(return_value="https://dog.ceo/api/breeds/list/all")
mocked_dogs.get_responce_code = MagicMock(return_value=200)
mocked_dogs.elements_count = MagicMock(return_value=100)
mocked_dogs.get_responce_status_by_entry = MagicMock(return_value=200)
mocked_dogs.get_total_breeds_count = MagicMock(return_value=2)
mocked_dogs.count_images_by_breed = MagicMock(return_value={"Yorkshire terrier": 23,
                                                            "Baskerville chihuahua": 1})


mocked_brew = Mock()
mocked_brew.name = MagicMock(return_value="https://api.openbrewerydb.org/breweries")
mocked_brew.get_responce_code = MagicMock(return_value=200)
mocked_brew.elements_count = MagicMock(return_value=20)
mocked_brew.get_count_by_state = MagicMock(return_value={"new_york": 15, "california": 20,
                                                         "arizona": 75, "alabama": 39, "ohio": 55})
mocked_brew.get_responce_status_by_endings = MagicMock(return_value=200)
mocked_brew.search_animals = MagicMock(return_value={"dog": 123, "cat": 764, "fish": 65})
mocked_brew.get_id_by_name = MagicMock(return_value=
                                       {"dog":
                                            ['530', '542', '1221', '2268', '3025', '3068', '3136', '4121', '4263',
                                             '4555', '5359', '5925', '7152', '7424', '7704'],
                                        "cooper":
                                             ['58', '3208', '6998', '7900', '3809', '3827', '4674', '5773', '6393',
                                              '6600', '7465', '3828', '2185', '4638', '4679'],
                                        "sisters":
                                             ['5961', '5960', '6930', '7715', '281', '6643']
                                         })


mocked_cdnjs = Mock()
mocked_cdnjs.name = MagicMock(return_value="https://api.cdnjs.com/libraries")
mocked_cdnjs.get_responce_code = MagicMock(return_value=200)
mocked_cdnjs.get_responce_code_by_entry = MagicMock(return_value=200)
mocked_cdnjs.elements_count = MagicMock(return_value=40)
mocked_cdnjs.search_by_text = MagicMock(return_value={"bootstrap": 185, "alert": 25})
mocked_cdnjs.match_number_by_field = MagicMock(return_value={"version": 20, "description": 20, "homepage": 20,
                                                             "keywords": 20, "license": 20,
                                                             "repository": 20, "autoupdate": 20, "author": 20,
                                                             "assets": 20})
