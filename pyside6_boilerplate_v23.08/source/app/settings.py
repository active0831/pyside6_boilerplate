# core
PATH_BASE = "./bin/"
PATH_TEMP = PATH_BASE+"temp/"

# addon.auth
AUTH_HOST_DEFAULT = "http://localhost:8000/"
AUTH_REST_API = {
    "LOGIN": "/users/login/", #post
    "LOGOUT": "/users/logout/", #get
    "CHECK_LOGIN_USER": "/users/user/", #get
}
AUTH_AUTO_LOGIN = True
