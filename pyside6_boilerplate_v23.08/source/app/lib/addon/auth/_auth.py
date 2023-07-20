import requests, json

from lib.core.state import AbstractState

from settings import *

class State(AbstractState):
    def __init__(self):
        super().__init__()        
        self.use("cookies",[{}])
        self.use("auth_host",[AUTH_HOST_DEFAULT])

        if AUTH_AUTO_LOGIN:
            try:
                with open(PATH_TEMP+"cookies.json", "r") as f:
                    cookies = json.load(f)
                    self.set("cookies",cookies,0)
            except:
                pass

def get(url, **kwargs):
    cookies = State().get("cookies")[0]
    kwargs["cookies"] = cookies

    auth_host = State().get("auth_host")[0]
    resp = requests.get(auth_host+url, **kwargs)

    cookies.update(requests.utils.dict_from_cookiejar(resp.cookies))
    State().set("cookies",cookies,0)

    return resp

def post(url, *args, **kwargs):
    cookies = State().get("cookies")[0]
    kwargs["cookies"] = cookies

    auth_host = State().get("auth_host")[0]
    resp = requests.post(auth_host+url, *args, **kwargs)

    cookies.update(requests.utils.dict_from_cookiejar(resp.cookies))
    State().set("cookies",cookies,0)    

    return resp

def login(user_auth_info):
    resp = post(AUTH_REST_API["LOGIN"],user_auth_info)

    if AUTH_AUTO_LOGIN:
        with open(PATH_TEMP+"cookies.json", "w") as f:
            json.dump(State().get("cookies")[0], f)

    return resp

def logout():
    resp = get(AUTH_REST_API["LOGOUT"])
    return resp

def check_login_user():
    resp = get(AUTH_REST_API["CHECK_LOGIN_USER"])
    return resp.text


