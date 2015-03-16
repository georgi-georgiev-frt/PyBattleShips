PyBattleShips
=============
[![Build Status](https://travis-ci.org/georgi-georgiev-frt/PyBattleShips.svg?branch=master)](https://travis-ci.org/georgi-georgiev-frt/PyBattleShips)
[![Coverage Status](https://coveralls.io/repos/georgi-georgiev-frt/PyBattleShips/badge.svg)](https://coveralls.io/r/georgi-georgiev-frt/PyBattleShips)

![PyBattleShips](/docs/images/game_snapshot.bmp?raw=true "PyBattleShips")

Console application - python single-player version of BattleShips game.

Installation
------------
Download this repository
    
    git clone https://github.com/georgi-georgiev-frt/PyBattleShips.git
    
(Optional but recommended) create virtualenv

    cd PyBattleShips
    virtualenv .
    
Install package requirements with pip

    pip install -r requirements.txt
    
Run the binary file

    cd PyBattleShips
    ./bin/battleships

Testing
-------

To run the tests:

    ./bin/runtests


Documentation
-------------

Developers documentation

    docs/readme.md
    
How to play
-----------

Enter your first guess where will be a ship:

![Missed shot](/docs/images/missed_shot.bmp?raw=true "Missed shot")

Missed! Try again:

![Right on target!](/docs/images/on_target.bmp?raw=true "Right on target!")

Let's sunk this ship!

![Sunk!](/docs/images/ship_sunk.bmp?raw=true "Sunk!")

Sunk all ships!

![Win!](/docs/images/game_complete.bmp?raw=true "Win!")

Won the game in 14 shots with only one wrong? How is this possible? Cheat applied:

![Cheat!](/docs/images/cheat_applied.bmp?raw=true "Cheat!")

