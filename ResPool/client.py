import types

__author__ = 'jason'
import sky_client
import utils


def add_res(name, model, update):
    """
    add a Res Object in ResPool
    :param name: name of the Res. Must be unique.
    :param model: model of the Res. Can be an JSON schema or just a JSON object for initial value.
    :param update: update method of the Res. This value can be a function , a dict or None.
        function: a function object or lambda object which accept the old value of this Res as the first parameter.
        dict: use one of default function. Format:
            {
                "method": "Time"/"Randint"/"FiniteStateMachine"/"NormalVariate"/"LinearClock",
                "some extra parameters....": "",
                ....
            }
        None: no update function. This Res only can be modified by its default set function.
    :return: true, if add resource is success.
    """
    update_function = None

    if utils.is_function(update):
        update_function = ["function", utils.function_to_string(update)]
    elif type(update) is dict and "method" in update:
        update_function = ["default", update]
    else:
        update_function = update

    content = sky_client.get_content(["res_pool", "add_res", [name, model, update_function]])
    sky_client.write(content)


def get_res_value(name, clock=-1):
    content, cid = sky_client.get_content(["res_pool", "get_res", [name, clock]], return_id=True)
    sky_client.write(content)

    result_template = sky_client.get_content(["res_pool_client", "get_res", cid, "?"])
    result = sky_client.read(result_template)
    if result is None or len(result) < 3:
        print "update_res Failed"
        return None
    else:
        return result[3]


def update_res(name, cycle=None, param=None):
    content, cid = sky_client.get_content(["res_pool", "update_res", [name, cycle, param]], return_id=True)
    sky_client.write(content)

    result_template = sky_client.get_content(["res_pool_client", "update_res", cid, "?"])
    result = sky_client.read(result_template)
    if result is None or len(result) < 3:
        print "update_res Failed"
        return None
    else:
        return result[3]


def get_clock():
    content, cid = sky_client.get_content(["res_pool", "get_clock", []], return_id=True)
    sky_client.write(content)

    result_template = sky_client.get_content(["res_pool_client", "get_clock", cid, "?"])
    result = sky_client.read(result_template)
    if result is None or len(result) < 3:
        print "update_res Failed"
        return None
    else:
        return result[3]


def register_listener(ref_res, condition, action):
    condition_str = utils.function_to_string(condition)
    action_str = utils.function_to_string(action)
    tuple = ["res_pool", "add_listener", [ref_res, condition_str, action_str]]
    content, cid = sky_client.get_content(tuple, return_id=True)
    sky_client.write(content)

    result_template = sky_client.get_content(["res_pool_client", "add_listener", cid, "?"])
    result = sky_client.read(result_template)
    if result is None or len(result) < 3:
        print "update_res Failed"
        return None
    else:
        return result[3]


def ticktock(time):
    content = sky_client.get_content(["res_pool", "ticktock", time])
    sky_client.write(content)


def reset_res_pool():
    content = sky_client.get_content(["res_pool", "reset"])
    sky_client.write(content)