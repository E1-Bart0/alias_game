import logging
from pathlib import Path

from django.core.management import BaseCommand
from word.models import EasyWord, HardWord, MediumWord

logging.basicConfig(filename="words_db.log", level=logging.DEBUG)
DB = {"easy": EasyWord, "medium": MediumWord, "hard": HardWord}


def fill_db(path: Path, difficult: str):
    """Add words to DB

    :param path: Path to file with words
    :param difficult: Difficult of words wto save in Model
    :return: None
    """
    with open(path, mode="r", encoding="utf-8") as data_file:
        for index, line in enumerate(data_file.readlines()):
            try:
                word, img = map(str, line.split("; "))
                DB[difficult](word=word, img=img).save()
                logging.info(f"{word} saved")
            except Exception as err:
                logging.exception(f"Line #{index}: {line}\nErr: {err}")


class Command(BaseCommand):
    help = "Fill DB with words"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p", "--path", required=True, type=Path, help="path to file with words"
        )
        parser.add_argument(
            "-d",
            "--difficulty",
            required=True,
            type=str,
            help="difficult of words",
            choices=("easy", "hard", "medium"),
        )

    def handle(self, *args, **options):
        logging.info("Start add words to DB with difficult")
        path = options["path"]
        difficulty = options["difficulty"]
        fill_db(path, difficulty)
        logging.info("Words was added to db")
