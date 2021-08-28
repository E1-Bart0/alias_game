# Site for online Alias game

Currently, run on this URL: [ALIAS](http://158.101.175.185/)

## What is an Alias

Alias is a board game, where the objective of the players is to explain words to each other.
The game is played in teams of varying size, and fits well as a party game for larger crowds.
The game is very competitive.

## Rules

The player, in his turn, explains a word in cards while the rest part of his team is trying to guess this word.

The other team can monitor the timer. Of course, the other team can help or vise versa confuse guessing team.

The team which first guesses a certain amount of words is winning.

## How to play on this site

For more convenience, you can choose your name and color
by clicking on your color at the top of page in the right corner.
Also, you can use emoji instead of your nickname [EMOJI](https://unicode-table.com/ru/sets/emoji/).

- Create a room and choose settings game settings: the difficulty, words amount, and round time.
- Share the room's code with your friends.
- Join one of 2 teams.
- Press "Ready" button and wait for the others.
- The Host decides when the game start. Clicking "Start" button.
- The first player who is explaining words is starting a round.
- Explain words on cards and click "Guess" on the card if the word is guessed.
- When time is over, the turn will automatically switch to the other team.
- Continue while one of the teams will reach the needed amount of words.
- The game is finished.

## How to run on your machine

### Via Docker
**Requirements**: _Docker_, _Docker-compose_

```
cp .env.template .env
# If it needed change .env
make run_docker
```
It launched on http://127.0.0.1:8000/


### Local
**Requirements**: _Postgresql_ or _Docker_, _python 3.9_

**Virtual environment and ENV:**

```
python -m venv .venv
. .venv/bin/activate
make install_requirements

cp .env.template .env
# change .env: DATABASE_HOST=127.0.0.1
```

**Postgresql in Docker:**
```
docker-compose up -d alias_db
python alias/manage.py runserver
```

**Postgresql Local**

Needed in Postgresql:
- Create databases: _alias_db_ and _game_alias_user_
- Create user: _game_alias_user_
- Set user password: _game_alias_password_
- Give all privileges _game_alias_user_ on db: _alias_db_

```
python alias/manage.py runserver
```
It launched on http://127.0.0.1:8000/

### Deploy with Nginx
**Requirements**: _Docker_, _Docker-compose_

```
cp .env.template .env
make deploy
```
It launched on http://127.0.0.1:8000/

## env

|   keys            | DEPLOY  | Docker  |   Local   |
|  -------          | -----   |------   |    -----  |
| APP_HOST          | 0.0.0.0 | 0.0.0.0 | 127.0.0.1 |
| APP_PORT          |   80    |  8000   | 8000      |
| SECRET_KEY        | 015-ip(il1)_sd4mn1bh%$m$x3rl!ait1)u-+5i)dd7pcr4bp4 |||
| ALLOWED_HOSTS     | *                             |||
| DEBUG             | False   | True    |  True     |
| DATABASE_HOST     | alias_db| alias_db| 127.0.0.1 |
| DATABASE_PORT     | 5432                          |||
| DATABASE_NAME     | alias_db                      |||
| DATABASE_USER     | game_alias_user               |||
| DATABASE_PASSWORD | game_alias_password           |||
