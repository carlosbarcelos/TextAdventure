# Adventure (Working Title)
> An object-oriented text adventure

More information [here](https://docs.google.com/document/d/1iE4sgK5sljFo6jyxO-f0B7pypGGfGc1jh1qKKWn28WM/edit?usp=sharing).

## Installation
**NOTE**: Python 3.6 or higher is required.

\# clone the repo<br/>
`$ git clone https://github.com/carlosbarcelos/TextAdventure`

\# change the working directory to TextAdventure<br/>
`$ cd TextAdventure`

\# install the requirements<br/>
`$ pip install -r requirements.txt`

## Usage

```bash
$ adventure.py --help
usage: adventure.py [-h] [--map MAPSAVE] [--player PLAYERSAVE]
                    [--achievement ACHIEVEMENTSAVE]

TextAdventure: An object-oriented text adventure

optional arguments:
  -h, --help            show this help message and exit
  --map MAPSAVE         The save file for the world
  --player PLAYERSAVE   The save file for the player. Type only the file name,
                        without extension. Ex) Player_1
  --achievement ACHIEVEMENTSAVE
                        The achievements to use for this game
```

## Tests
Unit tests are contained in TextAdventure/test.

To run all unit tests for all test classes, use [nose](https://nose.readthedocs.io/en/latest/).

`$ nosetests`
