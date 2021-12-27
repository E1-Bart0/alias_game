import csv
from typing import Iterable, Optional

import requests
from bs4 import BeautifulSoup


def run(path: str, difficult: str) -> None:
    with open(f"{difficult}.txt", mode="w", encoding="utf-8") as writing_file:
        for word in read_word_from_file(path):
            img = parsing_img(word[0], difficult)
            writing_file.write(f"{word[0]}; {img}\n")


def read_word_from_file(path: str) -> Iterable[list]:
    with open(path, mode="r", encoding="utf-8") as file:
        return csv.reader(file)


def parsing_img(word: str, difficult: str) -> Optional[str]:
    word = word.replace(" ", "%20")
    if difficult == "hard":
        word += "%20кальян"
    url = f"https://www.google.com/search?q={word}&tbm=isch"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser", multi_valued_attributes=False)
    try:
        return soup.find("img", alt="")["src"]
    except Exception:
        return None


if __name__ == "__main__":
    run("hookah.csv", difficult="hard")
