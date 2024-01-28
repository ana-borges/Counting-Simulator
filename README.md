# 3, 2, 5... Can you count?

A game in which you need to count how many goats are on the screen! It's harder than it sounds ;)

## Assets

Goats: https://opengameart.org/content/mountain-goat-sprites

Font: https://www.dafont.com/minecraft.font

## Run and generate executable

### Requirements

- Repository is cloned
- A python environment with the packages listed in `requirements.txt`

### Run

```
python3 main-window.py
```

### Generate executable

Running the following will generate an executable in `dist`:
```
pyinstaller --onefile \
    --name 325-can-you-count \
    --add-data assets:assets \
    --add-data sounds:sounds \
    main-window.py
cp -r assets dist/
cp -r sounds dist/
```

The executable can be bundled for transport as follows:
```
tar -zcvf 3_2_5_can_you_count.tar.gz dist/
```

### Run from executable

1. Make sure you are in the same directory as the executable

2. Run it as usual for your OS
