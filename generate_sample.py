import json
import uuid
import random
import argparse
import datetime as dt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate 2 sample files to be used as testing input for the main module"
    )
    parser.add_argument(
        "--sample-size", type=int, help="the amount of logs to be generated"
    )
    args = parser.parse_args()
    max_size = args.sample_size if args.sample_size else random.randint(50000, 100000)

    languages = [
        "ab",
        "aa",
        "af",
        "ak",
        "sq",
        "am",
        "ar",
        "an",
        "hy",
        "as",
        "av",
        "ae",
        "ay",
        "az",
        "bm",
        "ba",
        "eu",
        "be",
        "bn",
        "bh",
        "bi",
        "bs",
        "br",
        "bg",
        "my",
        "ca",
        "ch",
        "ce",
        "ny",
        "zh",
        "cv",
        "kw",
        "co",
        "cr",
        "hr",
        "cs",
        "da",
        "dv",
        "nl",
        "dz",
        "en",
        "eo",
        "et",
        "ee",
        "fo",
        "fj",
        "fi",
        "fr",
        "ff",
        "gl",
        "ka",
        "de",
        "el",
        "gn",
        "gu",
        "ht",
        "ha",
        "he",
        "hz",
        "hi",
        "ho",
        "hu",
        "ia",
        "id",
        "ie",
        "ga",
        "ig",
        "ik",
        "io",
        "is",
        "it",
        "iu",
        "ja",
        "jv",
        "kl",
        "kn",
        "kr",
        "ks",
        "kk",
        "km",
        "ki",
        "rw",
        "ky",
        "kv",
        "kg",
        "ko",
        "ku",
        "kj",
        "la",
        "lb",
        "lg",
        "li",
        "ln",
        "lo",
        "lt",
        "lu",
        "lv",
        "gv",
        "mk",
        "mg",
        "ms",
        "ml",
        "mt",
        "mi",
        "mr",
        "mh",
        "mn",
        "na",
        "nv",
        "nd",
        "ne",
        "ng",
        "nb",
        "nn",
        "no",
        "ii",
        "nr",
        "oc",
        "oj",
        "cu",
        "om",
        "or",
        "os",
        "pa",
        "pi",
        "fa",
        "pl",
        "ps",
        "pt",
        "qu",
        "rm",
        "rn",
        "ro",
        "ru",
        "sa",
        "sc",
        "sd",
        "se",
        "sm",
        "sg",
        "sr",
        "gd",
        "sn",
        "si",
        "sk",
        "sl",
        "so",
        "st",
        "es",
        "su",
        "sw",
        "ss",
        "sv",
        "ta",
        "te",
        "tg",
        "th",
        "ti",
        "bo",
        "tk",
        "tl",
        "tn",
        "to",
        "tr",
        "ts",
        "tt",
        "tw",
        "ty",
        "ug",
        "uk",
        "ur",
        "uz",
        "ve",
        "vi",
        "vo",
        "wa",
        "cy",
        "wo",
        "fy",
        "xh",
        "yi",
        "yo",
        "za",
        "zu",
    ]

    clients = ["easyjet", "booking", "rovio", "under-armour", "pinterest", "facebook"]

    logs = []
    timestamp = dt.datetime.now() + dt.timedelta(days=random.randint(-365, 365))
    for i in range(max_size):
        timestamp += dt.timedelta(
            minutes=random.randint(-10, 10),
            seconds=random.randint(-30, 30),
            microseconds=random.randint(-1000000, 1000000),
        )
        translation_id = uuid.uuid1().hex
        chosen_languages = random.sample(languages, 2)
        source_language = chosen_languages[0]
        target_language = chosen_languages[1]
        client_name = random.choice(clients)
        event_name = "translation_delivered"
        nr_words = random.randint(1, 100)
        duration = random.randint(5, 2000)
        random_log = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "translation_id": translation_id,
            "source_language": source_language,
            "target_language": target_language,
            "client_name": client_name,
            "event_name": event_name,
            "nr_words": nr_words,
            "duration": duration,
        }
        print(f"[{len(logs):06}] => {random_log}")
        logs.append(random_log)
    with open("sample.txt", "w") as line_file:
        line_file.write("\n".join([json.dumps(log) for log in logs]))
    with open("sample.json", "w") as json_file:
        json_file.write(json.dumps(logs) + "\n")
    print("Job done! Bye")
