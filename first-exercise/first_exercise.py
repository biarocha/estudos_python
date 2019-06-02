import json
import sys


def read_input_from_json_file():
    # read file input.json (or another file passed as input) and save
    # content as separate dictionaries for account, transactions and last_transactions
    # Example: python first_exercise.py input.json
    try:
        input_filename = sys.argv[-1]
        with open(input_filename, 'r') as input_file:
            input_data = input_file.read()

        input_dict = json.loads(input_data)
        return input_dict
    except Exception:
        print("Could not read input.json file")
        print("Try to run: python first_exercise.py input.json")


def check_if_transaction_is_above_limit():
    # check if current transaction is above the account limit and if it is above 90% of the limit
    output = {
        "approved": None,
        "newLimit": None,
        "deniedReasons": None
    }
    input_dict = read_input_from_json_file()
    if ((input_dict["transaction"]["amount"]) < (input_dict["account"]["limit"])) and ((input_dict["transaction"]["amount"]) <= ((input_dict["account"]["limit"] * 90) / 100)):
        output["approved"] = True
        return output
    else:
        output["approved"] = False
        output["deniedReasons"] = "Transaction amount above account limit"
        return output


def check_if_card_is_blocked():
    # check if card is blocked
    output = {
        "approved": None,
        "newLimit": None,
        "deniedReasons": None
    }
    input_dict = read_input_from_json_file()
    if input_dict["account"]["cardIsActive"] is True:
        output["approved"] = True
        return output
    else:
        output["approved"] = False
        output["deniedReasons"] = "Card is Blocked"
        return output


def check_blacklist():
    # check if current transaction merchant is in blacklist
    output = {
        "approved": None,
        "newLimit": None,
        "deniedReasons": None
    }
    input_dict = read_input_from_json_file()
    blacklist = input_dict["account"]["blacklist"]
    if input_dict["transaction"]["merchant"] in blacklist:
        output["approved"] = False
        output["deniedReasons"] = "Merchant in Blacklist"
        return output
    else:
        output["approved"] = True
        return output


def check_same_merchant():
    # check if there are more than 10 transactions on the same merchant
    output = {
        "approved": None,
        "newLimit": None,
        "deniedReasons": None
    }
    input_dict = read_input_from_json_file()
    last_transactions = input_dict["last_transactions"]
    from collections import Counter
    counter = Counter(key['merchant'] for key in last_transactions)
    freq_dict = [{'merchant': key, 'freq': value} for key, value in counter.items()]

    for item in freq_dict:
        if item['freq'] >= 10:
            if input_dict["transaction"]["merchant"] == item['merchant']:
                output["approved"] = False
                output["deniedReasons"] = "More than 10 transaction in the same merchant"
                return output
            else:
                output["approved"] = True
                return output


def check_time():
    # check if there are more than 3 transactions on a 2 minutes interval
    from datetime import datetime, timedelta
    output = {
        "approved": None,
        "newLimit": None,
        "deniedReasons": None
    }
    control_time = timedelta(hours=0, minutes=2, seconds=0)

    '#parsing last transactions times to datetime list'
    input_dict = read_input_from_json_file()
    last_transactions = input_dict["last_transactions"]
    date_time_list = ([d['time'] for d in last_transactions])
    datetime_object = []
    for i in date_time_list:
        datetime_object.append(datetime.strptime(i, '%Y-%m-%d %H:%M:%S'))

    '#parsing current transaction time'
    current_transaction_time = input_dict["transaction"]["time"]
    current_transaction_time_object = datetime.strptime(current_transaction_time, '%Y-%m-%d %H:%M:%S')

    '#checking if there are more than 3 last transactions with less than 2 minutes interval'
    if ((current_transaction_time_object - datetime_object[-1]) + (datetime_object[-1] - datetime_object[-2])
            + (datetime_object[-2] - datetime_object[-3])) <= control_time:
        output["approved"] = False
        output["deniedReasons"] = "More than 3 transactions on a 2 minutes interval"
        return output
    else:
        output["approved"] = True
        return output


def check_full_operation():
    # check all transaction rules and set the final result for the current transaction
    input_dict = read_input_from_json_file()
    operation_output = {
        "approved": None,
        "newLimit": None,
        "deniedReasons": None
    }

    '#verifying rules'
    output_limit = check_if_transaction_is_above_limit()
    output_blocked = check_if_card_is_blocked()
    output_blacklist = check_blacklist()
    output_same_merchant = check_same_merchant()
    output_time_interval = check_time()

    '#setting the final result based on rules verification'
    if (output_limit["approved"] and output_blocked["approved"] and output_blacklist["approved"] and
            output_same_merchant["approved"] and output_time_interval["approved"]) is True:
        new_limit = (input_dict["account"]["limit"]) - (input_dict["transaction"]["amount"])
        operation_output["approved"] = True
        operation_output["newLimit"] = new_limit
        return operation_output
    else:
        operation_output["approved"] = False
        operation_output["newLimit"] = input_dict["account"]["limit"]
        if output_blocked["deniedReasons"]:
            operation_output["deniedReasons"] = output_blocked["deniedReasons"]
        else:
            if output_blacklist["deniedReasons"]:
                operation_output["deniedReasons"] = output_blacklist["deniedReasons"]
            else:
                if output_same_merchant["deniedReasons"]:
                    operation_output["deniedReasons"] = output_same_merchant["deniedReasons"]
                else:
                    if output_time_interval["deniedReasons"]:
                        operation_output["deniedReasons"] = output_time_interval["deniedReasons"]
                    else:
                        if output_limit["deniedReasons"]:
                            operation_output["deniedReasons"] = output_limit["deniedReasons"]

    return operation_output


def write_output_in_json_file():
    # write the current transaction result to the output.json file
    try:
        full_operation_dict = check_full_operation()
        print(full_operation_dict)

        with open('output.json', 'a') as json_file:
            json.dump(full_operation_dict, json_file, indent=2)
            json_file.write('\n')
    except TypeError:
        print("Type error! Check input file")
    except ValueError:
        print("Value error! Check input file")
    except Exception:
        print("Unknown error! Could not save output.json file")


def update_input_file():
    # update the input file with new transaction and new limit if the transaction is approved
    try:
        input_filename = sys.argv[-1]
        full_operation_dict = check_full_operation()

        '#loading input.json file to dictionary that will be updated'
        if full_operation_dict["approved"] is True:
            input_update = read_input_from_json_file()

            '#loading input.json file to dictionary that will keep original values'
            input_original = read_input_from_json_file()

            '#updating dictionary values'
            input_update["account"]["limit"] = full_operation_dict["newLimit"]
            input_update["last_transactions"].append(input_original["transaction"])

            '#updating input.json file content'
            with open(input_filename, 'w') as file:
                json.dump(input_update, file, indent=4)

    except Exception:
        print("Could not update input.json file")


write_output_in_json_file()
#update_input_file()
