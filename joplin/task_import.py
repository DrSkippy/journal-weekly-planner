__version__ = "v0.1.0"

import requests
import sys
import re
import json
import datetime

FMT = "%Y-%m-%d_%H:%M"
MARKER_STR = "###NOZBE"
EXTRACTED_MARKER = ">>> Note updated by Nozbe Task Extractor"

task_re = re.compile(f"{MARKER_STR}.*{MARKER_STR}", re.IGNORECASE | re.MULTILINE)

token = "7a12bb249f8374b2413fae6094401dce3347215c5e9c19391ec94121d1233dbe8d8e50468a08f96c076b12b5552071bcc60b1e123cb7440ec6162e6f63a6568e"
token_parameter = f"token={token}"
port = 41184
ubuntu_desktop_url_base = f"http://localhost:{port}/"


def ping():
    url = ubuntu_desktop_url_base + f"ping"
    print(url)
    print(requests.get(url))


def extract_folder_id(items, title):
    for x in items:
        if x["title"] == title:
            return x["id"]


def get_task_folder_id(title="@nozbe"):
    url = ubuntu_desktop_url_base + f"folders?fields=id,title&{token_parameter}"
    result = requests.get(url)
    folder_id = extract_folder_id(result.json()["items"], title)
    return folder_id


def extend_task_and_defaults(task_dict, note_id):
    newline = f"Joplin Importer Version={__version__} at {datetime.datetime.now().strftime(FMT)}"
    newline += f"\nTasks associated with NoteID={note_id}"
    task_dict["note_id"] = note_id
    if task_dict["notes"] is None or task_dict["notes"] == "":
        task_dict["notes"] = newline
    else:
        task_dict["notes"] += f"\n{newline}"
    if task_dict["due_date"] is None or task_dict["due_date"] == "":
        task_dict["due_date"] = datetime.date.today().strftime("%Y-%m-%d")
    task_dict['hash_tags'] = [x for x in task_dict['hash_tags'] if x is not None and x != ""]
    return task_dict


def flatten(l):
    return [item for sublist in l for item in sublist]


def extract_tasks(notes_bodies):
    res = []
    for x in notes_bodies:
        note_id = x["id"]
        if x["body"].strip().startswith(EXTRACTED_MARKER):
            continue
        ts_blocks = task_re.findall(x["body"].replace("\n", ""))
        ts_clean_blocks = [x.strip(MARKER_STR) for x in ts_blocks]
        rec_blocks = [json.loads(z) for z in ts_clean_blocks]
        for rec in flatten(rec_blocks):
            extended_rec = extend_task_and_defaults(rec, note_id)
            if "title" in extended_rec and extended_rec["title"] is not None and extended_rec["title"] != "":
                res.append(extended_rec)
    return res


def get_notes_tasks_list():
    folder_id = get_task_folder_id()
    url = ubuntu_desktop_url_base + f"folders/{folder_id}/notes?fields=id,body&{token_parameter}"
    result = requests.get(url)
    notes_bodies = result.json()["items"]
    tasks = extract_tasks(notes_bodies)
    return tasks


def update_notes(id_list):
    for id in id_list:
        url = ubuntu_desktop_url_base + f"notes/{id}?fields=id,body&{token_parameter}"
        result = requests.get(url)
        notes_body = result.json()
        body = notes_body["body"]
        newline = EXTRACTED_MARKER + f" {datetime.datetime.now().strftime(FMT)}\n\n"
        body = newline + body
        url1 = ubuntu_desktop_url_base + f"notes/{id}?{token_parameter}"
        payload = json.dumps({"body": body})
        result = requests.put(url1, data=payload)
        print(f"id={id} response={result.status_code}", file=sys.stderr)


if __name__ == "__main__":
    note_tasks = get_notes_tasks_list()
    print(note_tasks)
    update_notes([note_tasks[0]["note_id"]])
