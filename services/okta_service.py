from loguru import logger
from okta.client import Client as OktaClient
from pathlib import Path
from services import utility_service
from services.cache_service import BasicCache

SERVICE_NAME = "okta"
DATA_LOCATION = "okta_data"


config = utility_service.load_yaml_data(Path("configs") / "okta.yaml")
okta_client = OktaClient(config['okta']['client'])
service_cache = BasicCache(DATA_LOCATION)


async def list_employees(query_params: list[str]) -> str:
    """Chat functionality that lists employees in an okta instance.

    Parameters
    ----------
    query_params : list[str]
        The query param tokens given in the chat.  They are unused in this method.

    Returns
    -------
    str
        The message to be displayed in the chat.
    """
    users, _, _ = await okta_client.list_users()
    cache_users(users)

    output = []
    for user in users:
        first_name = user.profile.firstName
        last_name = user.profile.lastName
        email = user.profile.email
        full_name = ", ".join([first_name, last_name])
        message = " - ".join([full_name, email])
        output.append(message)

    return "Employees:\n" + "\n".join(output)


async def update_employee(query_params: list[str]) -> str:
    """Chat functionality that updates an employee in an okta instance.

    Parameters
    ----------
    query_params : list[str]
        The query param tokens given in the chat.

    Returns
    -------
    str
        The message to be displayed in the chat.
    """
    try:
        email = utility_service.extract_email(query_params[0])
    except IndexError as e:
        logger.exception(f"ERROR: {e}")
        return "Sorry, did you give an email?"

    assignments = utility_service.extract_assignments(query_params[1:])
    if "users" in service_cache[DATA_LOCATION] \
    and email in service_cache[DATA_LOCATION]["users"]:
        user = service_cache[DATA_LOCATION]["users"][email]
        # Since the user info we have is in a cache, it could be stale.
        # Refetch
        user, _, _ = await okta_client.get_user(user.id)

    else:
        users, _, _ = await okta_client.list_users()
        cache_users(users)
        user = service_cache[DATA_LOCATION]["users"][email]

    for field, value in assignments.items():
        setattr(user.profile, field, value)

    user, resp, err = await okta_client.update_user(user.id, user)

    if not (is_response_ok := resp.get_status() == 200):
        logger.debug(f"Status was not ok {resp.get_status()} \n{err}")


    message = f"[Update: {'Success' if is_response_ok else 'Failure'}]\n"
    message += "\n".join([f"{field.capitalize()}: {value}"
                            for field, value in assignments.items()])
    return message


async def query_employee(query_params: list[str]) -> str:
    """Chat functionality that gets an employees data specified in an okta instance.

    Parameters
    ----------
    query_params : list[str]
            The query param tokens given in the chat.

    Returns
    -------
    str
        The message to be displayed in the chat.
    """
    try:
        email = utility_service.extract_email(query_params[0])
    except IndexError:
        return "Sorry, did you give an email?"

    users, _, _ = await okta_client.list_users()
    cache_users(users)

    try:
        if email in service_cache[DATA_LOCATION]["users"]:
            profile = service_cache[DATA_LOCATION]["users"][email].profile
            message = "\n".join([f"{attr.capitalize()}: {getattr(profile, attr)}"
                                    for attr in query_params[1:]])
            return f"Email: {email}\n" + message
    except AttributeError as e:
        logger.exception(f"ERROR: {e}")
        return "It looks like one of the query params isn't a part of the user"

    return f"Sorry, no user found with the email {email}."


async def create_employee(query_params: list[str]) -> str:
    """Chat functionality that creates an employee in an okta instance

    Parameters
    ----------
    query_params : list[str]
            The query param tokens given in the chat.

    Returns
    -------
    str
        The message to be displayed in the chat.
    """
    try:
        email = utility_service.extract_email(query_params[0])
    except IndexError:
        return "Sorry, did you give an email?"

    assignments = utility_service.extract_assignments(query_params[1:])
    profile_data = {**assignments, "email": email}
    user_request = {"profile": {**profile_data,
                                "login": email}}

    _, resp, err = await okta_client.create_user(user_request)

    if not (is_response_ok := resp.get_status() == 200):
        logger.debug(f"Status was not ok {resp.get_status()} \n{err}")


    message = f"[Creation: {'Success' if is_response_ok else 'Failure'}]\n"
    message += "\n".join([f"{field.capitalize()}: {value}"
                            for field, value in profile_data.items()])
    return message


def cache_users(user_list: list[object]):
    """Conveniently cache a list of users objects as a dictionary.

    Parameters
    ----------
    user_list : list[object]
        The user objects that are found in the Okta-python SDK.
    """
    # creating easy access of user data
    email_user_dict = {user.profile.email:user for user in user_list}

    # Caching since users will have their ids and
    # and rather than searching through a list again, just pull
    # the user from the cache and update the info when needed
    service_cache[DATA_LOCATION] = {"users": email_user_dict}


def get_handler_registry() -> dict:
    """Return a list of registered handlers for chat queries.

    Handler registration is explicit in code and functionality is not added
    dynamically.

    Returns
    -------
    dict
        A dictionary with a keys as the verbs and function handlers as the values.
    """
    return {SERVICE_NAME: {"list": list_employees,
                           "update": update_employee,
                           "query": query_employee,
                           "create": create_employee}}

