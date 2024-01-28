# 325: Can you Count?

A game in which you need to count how many objects are on the screen! It's harder than it sounds ;)

## Generate executable

Requirements:
- Repository is cloned
- A python environment with the packages listed in `requirements.txt`

Running the following will generate an executable in `dist`:
```
pyinstaller --onefile \
    --name 325-can-you-count \
    --add-data assets:assets \
    --add-data sounds:sounds \
    main-window.py
```
