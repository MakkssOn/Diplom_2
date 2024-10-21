
class Urls:
    HOST = "https://stellarburgers.nomoreparties.site"
    CREATE_USER = f"{HOST}/api/auth/register"
    DELETE_USER = f"{HOST}/api/auth/user"
    LOGIN_USER = f"{HOST}/api/auth/login"
    REPLACE_DATA = f"{HOST}/api/auth/user"
    CREATE_ORDER = f"{HOST}/api/orders"
    GET_ORDER = f"{HOST}/api/orders"


class TextAnswer:
    TRUE = 'success":true'
    FALSE = '"success": false'
    ALREADY_EXISTS = "User already exists"
    INCORRECT_DATA = "email or password are incorrect"
    UNAUTHORIZED = "You should be authorised"
    NOT_INGREDIENT = "Ingredient ids must be provided"
    ORDER_INCORRECT_INGREDIENTS = 'Internal Server Error'
    ORDER_WITHOUT_AUTH = 'You should be authorised'


class Ingredients:
    BUN = "61c0c5a71d1f82001bdaaa6d"
    MEAT = '61c0c5a71d1f82001bdaaa6f'
    KOKLETA = '61c0c5a71d1f82001bdaaa71'
    SAUCE = '61c0c5a71d1f82001bdaaa72'
    ENIGMA = '00000000000000000000000000'

