import zipcodes
from airports import airports
from standardAbbr import state_abbr, valid_states

def clean_data(query):
    query["Current Street"] = query["Current Street 1"] + " " + query["Current Street 2"]
    query["Previous Street"] = query["Previous Street 1"] + " " + query["Previous Street 2"]
    (c, z, s) = fill_attempt(query["Current City"], query["Current Zip Code"], query["Current State"])
    query["Current City"] = c
    query["Current Zip Code"] = z
    query["Current State"] = s
    (c, z, s) = fill_attempt(query["Previous City"], query["Previous Zip Code"], query["Previous State"])
    query["Previous City"] = c
    query["Previous Zip Code"] = z
    query["Previous State"] = s
    return query

def fill_attempt(ocity, ozipcode, ostate):
    city = ocity
    zipcode = ozipcode
    state = ostate
    try:
        city = city.lower() if city.lower() else ""
        state = state_abbr.get(state.lower(), state.lower())
        zipcode = "".join(char for char in zipcode if char.isdigit())
        # incase it's an airport lol
        city = airports.get(city, city)
        search_zip = zipcodes.matching(zipcode) if zipcode != "" else []
        search_zip = {} if len(search_zip)==0 else search_zip[0]
        search_city = zipcodes.filter_by(city=city)
        # We have a zip and a state.
        if city == "" and zipcode != "":
            city = search_zip['city']
        elif zipcode == "" and search_city != []:
            for i in search_city:
                if i["state"].lower() == state:
                    zipcode = i["zipcode"]
        elif (state == "" or state not in valid_states) and search_zip != {}:
            state = search_zip['state']
        elif state == "" and search_city != []:
            for i in search_city:
                if i["zipcode"] == zipcode:
                    state = i["state"].lower()
    except:
        return (ocity, ozipcode, ostate)
    return(city, zipcode, state)
