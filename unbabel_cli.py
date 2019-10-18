import re
import sys
import json
import heapq
import argparse
import datetime as dt


class CustomParser(argparse.ArgumentParser):
    """Class to show the help message when there is an error when parsing the
        arguments
    """

    def error(self, message):
        """Method called when some error occurs during the argument parsing

        Arguments:
            message {string} -- the message explaining the error
        """
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


class TranslationLogItem(dict):
    """Class that inherits from dict to enable the usage of getters
    and setters that are already implemented in the dict class
    """

    def __init__(self, jsonDict):
        """initializes the log using a object that was parsed from json

        Arguments:
            jsonDict {dict} -- object parsed from json containing the
            following properties: timestamp, translation_id, source_language,
            target_language, client_name, event_name, duration, nr_words
        """
        props = [
            "timestamp",
            "translation_id",
            "source_language",
            "target_language",
            "client_name",
            "event_name",
            "duration",
            "nr_words",
        ]
        # Copy the properties from jsonDict to itself
        try:
            for prop in props:
                self[prop] = jsonDict[prop]
        except KeyError as e:
            print(f"Error when trying to copy the object's properties.\n{e}")
            raise e
        # Parse datetime string using the following format "2018-12-26 18:12:19.903159"
        self.datetime = dt.datetime.strptime(self.timestamp, "%Y-%m-%d %H:%M:%S.%f")

    def __getattr__(self, attr):
        """override the '.'(dot) operator to allow using the syntax self.attribute

        Arguments:
            attr {string} -- attribute to be returned
        """
        return self.get(attr)

    def __setattr__(self, key, value):
        """override the '.'(dot) operator to allow using the syntax self.attribute

        Arguments:
            key {string} -- key to be updated/created
            value {any} -- the value to be saved
        """
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        """override the '[]'(brackets) operator to allow using the syntax self['attribute']

        Arguments:
            key {string} -- key to be updated/created
            value {any} -- the value to be saved
        """
        super(TranslationLogItem, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        """override the '.'(dot) operator to allow using the syntax self.attribute

        Arguments:
            attr {string} -- attribute to be deleted
        """
        self.__delitem__(item)

    def __delitem__(self, key):
        """override the '[]'(brackets) operator to allow using the syntax self['attribute']

        Arguments:
            key {string} -- key to be deleted
        """
        super(TranslationLogItem, self).__delitem__(key)
        del self.__dict__[key]

    def __lt__(self, other):
        """override the '<'(less than) operator to allow comparing with other TranslationLogItem

        Arguments:
            other {TranslationLogItem} -- the other TranslationLogItem that will be compared to this one
        """
        return self.datetime < other.datetime


def ceiling_minute(datetime_obj):
    """Round up the minute of a datetime object by clearing the seconds and microseconds
    if existing or keeps it unchanged if not

    Arguments:
        datetime_obj {datetime.datetime} -- the object to be rounded up
    """
    if datetime_obj.second or datetime_obj.microsecond:
        #   When we add the remaining microseconds, it ends up being nomalized to
        # one full second, so we need to count for it when summing the remaining
        # seconds
        return datetime_obj + dt.timedelta(
            seconds=59 - datetime_obj.second,
            microseconds=1000000 - datetime_obj.microsecond,
        )
    else:
        return datetime_obj

def __get_item_list(input_file):
    """Gets the item list from the input file

    Arguments:
        input_file {string} -- the file that will be parsed

    Raises:
        Exception: When the file is not parseable it raises an exception

    Returns:
        list -- the list containing the items parsed from the input_file
    """
    with open(input_file, "r") as file_obj:
        file_text = file_obj.read()
        try:
            # Try to load the file content as json
            item_list = json.loads(file_text)
            if not isinstance(item_list, list):
                # If it's not a list create one containing the object
                item_list = [item_list]
        except Exception:
            # If loading the json fails, attemp to parse line by line
            try:
                lines = re.split("[\r\n]+", file_text)
                item_list = [json.loads(line) for line in lines]
                # # Easier to debug when decoupled
                # item_list = []
                # for line in lines:
                #     item_list.append(json.loads(line))
            except json.JSONDecodeError as je:
                print(f"Error while parsing the json lines: {je}")
                raise Exception("Parsing lines error")
        return item_list


def calc_moving_avg(input_file, window_size=10, property_name="duration"):
    """Calculates the moving average, from a given window size, split by minute
    from the earliest entry up to the latest entry

    Arguments:
        input_file {sting} -- the path to the file containing the data

    Keyword Arguments:
        window_size {int} -- the size of the window that will be averaged in
                                minutes (default: {10})
        property_name {string} -- the property that will be averaged it can be: "nr_words" or "duration" (default: {"duration"})

    Returns:
        {list} -- a list of objects containing the following properties:
                    date (string) and average_delivery_time (float)
    """
    item_list = __get_item_list(input_file)
    log_list = []
    # Convert the Json objects into Log objects
    for item in item_list:
        log = TranslationLogItem(item)
        heapq.heappush(log_list, log)

    # Get the earliest log entry
    current_log = heapq.heappop(log_list)
    # Add it to the window list
    logs_in_window = [current_log]
    # Set the sum of log chosen property in the window list, used to save processing time
    total_sum = current_log[property_name]
    # Ceil the datetime of the earliest log to include it in the results
    current_datetime = ceiling_minute(current_log.datetime)

    result = []
    while len(log_list) > 0:
        # Check if we need to remove logs that are inside the window
        lower_boundary = current_datetime - dt.timedelta(minutes=window_size)
        while logs_in_window[0].datetime < lower_boundary:
            # As the window list is sorted we don't need to search through the whole list
            popped_log = logs_in_window.pop(0)
            # To save processing time we remove the value from the total sum
            total_sum -= popped_log[property_name]
        # Then we run add all logs that are now in the window range
        while current_log.datetime < current_datetime and len(log_list) > 0:
            current_log = heapq.heappop(log_list)
            logs_in_window.append(current_log)
            # Add their values to the total
            total_sum += current_log[property_name]
        # Increase 1 minute to the current time
        current_datetime += dt.timedelta(minutes=1)
        # The average can be calculated using the variable instead of going through the list
        average = total_sum / len(logs_in_window)
        result.append(
            {
                # Convert it to string to make it compliant with the requested output
                "date": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "average_delivery_time": average,
            }
        )
    return result


def get_clients_report(input_file):
    """Get the clients report containing the list of clients and the amount of translations done

    Arguments:
        input_file {string} -- the path to the file to be parsed

    Returns:
        list -- An list of objects in the following format { client_name: {string}, translation_count: {int}}
    """
    item_list = __get_item_list(input_file)
    clients = {}
    for item in item_list:
        log = TranslationLogItem(item)
        try:
            clients[log.client_name] += 1
        except:
            clients[log.client_name] = 1
    return [{"client_name":client, "translation_count":count} for (client, count) in clients.items()]


def get_languages_report(input_file):
    """Get the languages report containing all languages pairs and theirs respective usage count

    Arguments:
        input_file {string} -- the path to the file to be parsed

    Returns:
        list -- An list of objects in the following format { source_language: {string}, target_language: {string}, translation_count: {int}}
    """
    item_list = __get_item_list(input_file)
    languages = {}
    for item in item_list:
        log = TranslationLogItem(item)
        lang_pair = f"{log.source_language}|{log.target_language}"
        try:
            languages[lang_pair] += 1
        except:
            languages[lang_pair] = 1
    return [{"source_language":langs.split("|")[0], "target_language":langs.split("|")[1], "translation_count":count} for (langs, count) in languages.items()]

if __name__ == "__main__":
    parser = CustomParser(
        description="Outputs the moving average "
        + "of the input file minute by minute."
    )
    parser.add_argument("--input-file", required=True, help="the file to be parsed")
    parser.add_argument(
        "--window-size",
        type=int,
        default=10,
        help="the window size, in minutes, that will be averaged",
    )
    parser.add_argument(
        "--property",
        required=False,
        default="duration",
        choices=["nr_words", "duration"],
        help="the property that will be averaged",
    )
    parser.add_argument(
        "--clients-report",
        required=False,
        action='store_true',
        help="if this option is present it shows a report with the amount of translations made by each client instead of the default behavior"
    )
    parser.add_argument(
        "--languages-report",
        required=False,
        action='store_true',
        help="if this option is present it shows a report with all the language pairs used instead of the default behavior"
    )

    args = parser.parse_args()
    if args.clients_report:
        for report in get_clients_report(args.input_file):
            print(report)
    elif args.languages_report:
        for report in get_languages_report(args.input_file):
            print(report)
    else:
        for avg in calc_moving_avg(args.input_file, args.window_size, args.property):
            print(avg)
