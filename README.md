# tournament-results
fsnd: a database to store the game matches between players and determine the winners of various games.

## Prerequirement

- Vagrant
- VirtualBox

## Run and Test

- start vagrant - `vagrant up`, `vagrant ssh`
- create database - `psql`, `create database tournament`
- create tables - `psql tournament`, `\i tournament.sql`
- run tests - `python tournament_test.py`
