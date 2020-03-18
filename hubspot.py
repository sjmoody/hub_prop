import json, requests, urllib, csv, datetime
import logging

logging.basicConfig(filename='logger.log', format='%(asctime)s Module %(module)s %(message)s',level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Initialized")


DEFAULT_APIKEY_VALUE = 'demo'
API_KEY = "?hapikey="
HS_API_URL = 'https://api.hubapi.com'
# CLIENT_API_KEY_VALUE = 
# DEMOAPIKEY = "?hapikey=" + APIKEY_VALUE
# CLIENT_API_KEY = "?hapikey=" + CLIENT_API_KEY_VALUE


# def get_key():
#     input_key = input("Enter API key (default demo returns HS demo data):")
#     if not input_key:
#         input_key = 'demo'
#     return input_key

def getAllEngagementsOnce(offset='', key_value=''):
    # Returns dict.  Access engagements as data['results'][<list>]
    if key_value == '':
        key_value = get_key()
    
    endpoint = '/engagements/v1/engagements/paged'
    
    if offset == '':
        url = HS_API_URL + endpoint + API_KEY + key_value + '&limit=250'     
    else:     
        url = HS_API_URL + endpoint + API_KEY + key_value + '&limit=250' + "&offset=" + str(offset)
    response = requests.get(url)
    response.raise_for_status()
    logger.info(f'Response: {response}')
    data = response.json()
    logger.info('data count returned:', len(data['results']))
    return data


def getAllEngagements():
    # Returns dict.  Access engagements as data['results'][<list>]
    logger.info("getting all engagements")    
    key_value = get_key()
    # first run: data is object with results, hasmore offset
    data = getAllEngagementsOnce(key_value=key_value) 
    results = data['results']    
    logger.info("first run completed.  Length of results: ", len(results))
    logger.info('results is of type', type(results))
    
    while(data['hasMore'] == True):
        logger.info("has more is ", data['hasMore'])
        logger.info('offset is ', data['offset'])
        logger.info("going to get more data")
        data = (getAllEngagementsOnce(key_value=key_value, offset=data['offset']))
        results.extend(data['results'])
        logger.info("len of results now ", len(results))
    return results

def getEngagement():
    pass

def getTotalNumberOfContacts(key_value=''):
    if key_value == '':
        key_value = get_key()
    endpoint = "/contacts/v1/contacts/statistics"
    url = HS_API_URL + endpoint + API_KEY + key_value
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    return data['contacts'] # returns integer


def getAllContactProperties(key_value=''):
    if key_value == '':
        print("fetching key")
        key_value = get_key()
    endpoint = '/properties/v1/contacts/properties'
    url = HS_API_URL + endpoint + API_KEY + key_value 
    print('fetching for url', url)
    response = requests.get(url) 
    response.raise_for_status()
    logger.info(f"response received: {response.status_code}") #200
    data = response.json()
    logger.info("data received: ")
    # print(data)
    property_list = data
    return property_list




def getAllContacts(property_list, key_value=''):
    if key_value == '':
        key_value = get_key()
    totalContacts = getTotalNumberOfContacts(key_value=key_value)
    max_results = totalContacts
    hapikey = key_value
    count = 100 
    contact_list = []

    
    property_list_str = '&property=' + '&property='.join(property_list)



    get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
    parameter_dict = {'hapikey': key_value, 
                      'count': count,                                            
                      }
    headers = {}
    logger.info(f"getting {max_results} contacts out of {totalContacts} total")
    
    # Paginate your request using offset
    has_more = True
    while has_more:
        logger.info(f"current progress: {len(contact_list)} of {max_results}")
        parameters = urllib.parse.urlencode(parameter_dict)
        get_url = get_all_contacts_url + parameters + property_list_str
        # print("requesting URL: ", get_url)
        r = requests.get(url= get_url, headers = headers)
        response_dict = json.loads(r.text)
        has_more = response_dict['has-more']
        contact_list.extend(response_dict['contacts'])
        parameter_dict['vidOffset']= response_dict['vid-offset']
        if len(contact_list) >= max_results: # Exit pagination, based on whatever value you've set your max results variable to. 
            logger.info('maximum number of results exceeded')
            break
    logger.info('loop finished')

    list_length = len(contact_list) 
    logger.info(f"results returned of type {type(contact_list)}")

    logger.info(f"You've succesfully parsed through {list_length} contact records and added them to a list")
    return contact_list


def saveAllContacts(property_name_list):
    #get all contacts 
    contact_list = getAllContacts(property_name_list)
    # contacts = []
    # for contact in contact_list:
    #     contacts.extend()
    
    # contacts = contact_list["properties"]

    # # This prints everything for every contact
    # for c in contact_list:
    #     print(c)


    # gets timestampe for filename 
    ts = int(datetime.datetime.now().timestamp())
    filename = 'hs_contact_list' + str(ts) + '.csv'
    logger.info('attempting to save file', filename)
    
    # opens file and writes rows for each contact 
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, property_name_list)
        writer.writeheader()
        i = 0
        for item in contact_list: # for each contact
            # print(f"value for contact {i}: ")
            # row = {}
            for k in item['properties']:
                
                row.update({k : item['properties'][k]['value']})
                # print(k, item['properties'][k]['value'])
            # print(item['properties'])            
            writer.writerow(row)
            
            i +=1
            # writer.writerow(row['properties'])
            
    # for key in contact_list[0]['properties']:
    #     print(key, '->', contact_list[0]['properties'][key]['value'])
    logger.info("file saved at: ", filename)
    

def saveAllContactProperties():
    property_list = getAllContactProperties(key_value='')
    print("collected properties.  Count: ", len(property_list))
    ts = int(datetime.datetime.now().timestamp())

    filename = "hs_property_list_" + str(ts) + '.csv'
    print("attempting save to file: ", filename)
    with open(filename, 'w', newline='')  as csvfile:
        # fieldNames = unknown?  Maybe can be default
        writer = csv.DictWriter(csvfile, property_list[0].keys())
        writer.writeheader()
        for row in property_list:
            writer.writerow(row)
    print("file saved at ", filename)