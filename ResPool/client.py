__author__ = 'jason'
import sky_client
import utils


def add_res(name, model, update):
    content = sky_client.get_content(["res_pool", "add_res", [name, model, utils.function_to_string(update)]])
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


