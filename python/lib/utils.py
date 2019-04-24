import requests
import ast
import time

def get_request(url, user=None, headers={}, request_wait_time=300.00):
    # print url
    if user:
        request = requests.get(url, auth=(user, ''), headers=headers)
    else:
        request = requests.get(url, headers=headers)
    # print request
    if request.status_code == 200:
        return request

    # too many requests
    if request.status_code == 429:
        print '*'*100
        print "Too Many Requests, wait for %s seconds" % str(request_wait_time)
        print '*'*100
        time.sleep(request_wait_time)
        return get_request(url, user, headers)
    
    # temporarily unavailable
    elif request.status_code == 503:
        print '*'*100
        print "Temporarily Unavailable, wait for %s seconds" % str(request_wait_time)
        print '*'*100
        time.sleep(request_wait_time)
        return get_request(url, user, headers)

    else:
        return request

def get_all_mps(theyworkyou_apikey):
	"""
    Function to return a full list of current MPs
    """
	url = 'https://www.theyworkforyou.com/api/getMPs?key=%s&output=js' % (theyworkyou_apikey)
	request = get_request(url=url, user=None, headers={})
	# literal eval the json request into actual json
	literal = ast.literal_eval(request.content)
	return literal

def get_member_image(member_id):
    url = 'http://data.parliament.uk/membersdataplatform/services/images/MemberPhoto/%s/Web Photobooks' % member_id
    response = requests.get(url, stream=True)
    return response.raw

def get_member_info(theyworkyou_apikey, person_id):
    url = 'https://www.theyworkforyou.com/api/getMPInfo?key=%s&id=%s&output=js' % (theyworkyou_apikey, person_id)
    request = get_request(url=url, user=None, headers={})
    # literal eval the json request into actual json
    return ast.literal_eval(request.content)