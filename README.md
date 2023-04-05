# Introduction

A project to learn assembly by creating my own pokemon save file

# Getting started

[There is no getting started]

# Non-project accomplishments

- Disassemble a pokemon game and save file by monitoring how bytes change between different states, and generally messing around
- Use a GUI debugger to watch changes in memory (All debuggers I used previously were CLI debuggers. Go figure)

# Perfect is the enemy of the good

- To implement jsonschema instead of Pydantic for data validation. Pydantic is an overkill, and is not as language-agnostic as Pydantic
- To reduce reliance on Pydantic to throw data validation errors. To substitute Pydantic exceptions with more descriptive and more context-specific exceptions
- To expose the main function with an API, preferably with Flask or Django. I am getting too comfortable with using FastAPI for literally every personal project that requires a Python web framework

# Learning points

- To stop overengineering things
- To stop privatising functions without good reason; functions should be public by default. My codebase is not 1980s Britain, and I am not Thatcher
- To use ChatGPT to elucidate poor documentation. The debugger I used, bgb had poor documentation. Thankfully, the debugger was based of (allegedly) many other debuggers which ChatGPT was able to pull from.
