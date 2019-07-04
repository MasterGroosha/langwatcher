# -*- coding: utf-8 -*-

from typing import Optional
from telethon.tl.types import LangPackString, LangPackStringPluralized, LangPackDifference
from time import gmtime, strftime
from pathlib import Path


async def prepare_dict(pack: LangPackDifference) -> Optional[dict]:
    result_dict = {}
    for string in pack.strings:
        if isinstance(string, LangPackString):
            result_dict[string.key] = string.value
        elif isinstance(string, LangPackStringPluralized):
            for quantifier in ['one', 'other']:  # those 2 keys are enough for English pack
                result_dict["{}_{}".format(string.key, quantifier)] = getattr(string, quantifier + "_value")
    return result_dict


async def generate_post(changes: dict) -> bool:
    elements = ["---\n",
                "title: Changes to {}\n".format(", ".join(platform for platform in changes)),
                "date: {}\n".format(strftime("%Y-%m-%d", gmtime())),
                "---\n"]

    for platform in changes:
        elements.append("<h3>{}</h3>\n".format(platform))
        if len(changes[platform]["new"]) > 0:
            elements.append("<h4>New strings:</h4>\n{{< highlight diff >}}\n")
            for item in changes[platform]["new"]:
                elements.append("+ {key}: {value}\n".format(key=item[0], value=item[1]))
            elements.append("{{< /highlight >}}\n\n")
        if len(changes[platform]["changed"]) > 0:
            elements.append("<h4>Changed strings:</h4>\n{{< highlight diff >}}\n")
            for item in changes[platform]["changed"]:
                elements.append("- {key}: {oldvalue}\n+ {key}: {newvalue}\n"
                                .format(key=item[0], oldvalue=item[1], newvalue=item[2]))
            elements.append("{{< /highlight >}}\n")

    # Hardcode :(
    file_path = Path(".").joinpath("..", "langwatcher-site", "content", "posts", strftime("%Y%m%d%H%M.md", gmtime()))
    with open(file_path.resolve(), "wt", encoding="utf-8") as outfile:
        outfile.writelines(elements)
    return True
