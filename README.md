# Introduction

A project to learn assembly by creating my own pokemon save file

# Getting started

[There is no getting started]

# Project accomplishments

- Allow users to configure their current party's pokemon including pokemon, name, and stats

# Non-project accomplishments

- Disassemble a pokemon game and save file by monitoring how bytes change between different states, and generally messing around
- Use a GUI debugger to watch changes in memory (All debuggers I used previously were CLI debuggers. Go figure)
- Learn a bit of assembly

# Perfect is the enemy of the good

- To implement jsonschema instead of Pydantic for data validation. Pydantic is an overkill, and is not as language-agnostic as Pydantic
- To reduce reliance on Pydantic to throw data validation errors. To substitute Pydantic exceptions with more descriptive and more context-specific exceptions
- To expose the main function with an API, preferably with Flask or Django. I am getting too comfortable with using FastAPI for literally every personal project that requires a Python web framework

# Learning points

- To stop overengineering things
- To stop privatising functions without good reason; functions should be public by default. My codebase is not 1980s Britain, and I am not Thatcher
- To use ChatGPT to elucidate poor documentation. The debugger I used, bgb had poor documentation. Thankfully, the debugger was based of (allegedly) many other debuggers which ChatGPT was able to pull from.

# Resources

(Gameboy emulator + debugger)[https://bgb.bircd.org/manual.html]
(Pokemon save files)[https://sites.google.com/site/torchickens2/pokemon-save-files]
(Pokemon save files)[https://www.zophar.net/savestates/gameboy/pokemon-red-version.html]
(Pokemon save files)[https://projectpokemon.org/home/forums/topic/7477-pokemon-redblueyellow-sav-file/]
(Gameboy programming manual)[https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiAivDg7pL-AhWQ4DgGHS_iDacQFnoECAsQAQ&url=https%3A%2F%2Farchive.org%2Fdownload%2FGameBoyProgManVer1.1%2FGameBoyProgManVer1.1.pdf&usg=AOvVaw3LoEvXhZRBH7r68qdXIhiP]
