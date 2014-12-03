import types

__author__ = 'jason'
import sky_client
import utils



def add_res_from_file(file_path, file_type="xml"):
    """
    add a Res from file.
    file format:
    <res_list>
    <res name="some name">
        <model>
            <format>
                number/dict/str/list
            </format>
            <initial>
                .... some basic value match the format.
            </initial>
        </model>
        <update>
            <delay>
                int value: number of clock for first update
            </delay>
            <next>
                1.int: const cycle length of one update
            </next>
            <rule>
                function.
            </rule>
        </update>
    <res>
    <res>some other res.</res>
    <res_list>

    the function's format:
    basic value type:
        1. int/float: 234 or 1.23
        2. list: [basic_value1, basic_value2]
        3. dict: { 'a' : basic_value }
        4. string: "some string"
        5. $name: a resource's value of last clock. $self for it's own value.
    function body format:
    <function name="function name" type="function type"> both type and name defines an function.
        <parameter name="parameter name">
            parameter value, can be a basic value or another function.
        </parameter>
        <parameter name="parameter name">
            this function may contains multi parameter.
        </parameter>
    </function>

    currently support the following function:
    type = math_expression
        name = add : a+b
            :parameter a,b: can be a basic value or a function
        name = division: a/b
        name = minus: a-b
        name = multiply: a*b
        name = mod: a mod b
        name = linear : ax+b
            :parameter a,b:
            :parameter x: it's usually $name.
        name = sin : asin(x)+b
        name = log : alog(x)+b
        name = sum : term1+term2+...
            :parameter term (multi): the adder.
    type = probability
        name = "markov_chain"
            :parameter state_set: list
            :parameter init_state: string, initial state.
            :parameter trans_matrix: float matrix, has the same size as state_set.
        name = "simple_rand" random int from [min, max]
        name = "normal_variate_rand":
            :parameter mu
            :parameter sigma
    type = others
        name = "combine"
            :parameter section (multi)
                <name></name>
                <value></value>
        name = "data_list"
            :parameter data: list

    :param file_path:
    :param file_type: only support xml for now.
    :return:
    """
    if file_type == "xml":
        data = utils.get_data_from_xml(file_path)
    else:
        print "unknown file_type"
        return

    print "res number:", len(data["res_list"]["res"])
    print data
    ret = list()
    for res in data["res_list"]['res']:
        name = res["@name"]
        model = res["model"]
        update = res["update"]
        add_res(name, model, utils.warp_update(update))
        ret.append(name)
    return ret


def add_res(name, model, update):
    """
    add a Res Object in ResPool
    :param name: name of the Res. Must be unique.
    :param model: model of the Res. Can be an JSON schema or just a JSON object for initial value.
    :param update: update method of the Res. This value can be a function , a dict or None.
        function: a function object or lambda object which accept the old value of this Res as the first parameter.
        dict: use one of default function. Format:
            {
                "method": "Time"/"Randint"/"MarkovChain"/"NormalVariate"/"LinearClock"...,
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