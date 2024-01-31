# 3, 2, 5 Can you count?

A game in which you need to count how many goats are on the screen! It's harder
than it sounds ;)

## Credits

This game was created as part of the [Global Game Jam 2024][GGJ] using
[pygame][pygame] and is licensed under [CC BY-NC-SA 4.0][CC-BY-NC-SA].

### Authors

- Ana Borges
- Nils Roth
- Jorge Simões

### Packages

The package [Pygame Text Input][textinput] is vendored instead of installed
because otherwise pygbag can't use it. It is distributed under the [MIT
License][MIT].

### Assets

The goat assets were created by [Sevarihk][goats] and are distributed under
[CC-BY 4.0][CC-BY].

The font is the [Minecraft Font by Craftron Gaming][font].


## Run and generate executable

### Requirements

- Repository is cloned
- A python environment with the packages listed in `requirements.txt`

### Run in a browser

From outside the git directory:
```
pygbag Counting-Simulator
```

Point your browser at http://localhost:8000 (or  http://localhost:8000#debug
for debugging purposes).

This doesn't work with Firefox, see [pygbag#129][issue-129].

### Run locally

```
python3 main.py
```

### Generate executable

Running the following will generate an executable in `dist`:
```
pyinstaller --onefile \
    --name 325-can-you-count \
    --add-data assets:assets \
    --add-data sounds:sounds \
    main.py
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

[pygame]: https://www.pygame.org/
[textinput]: https://github.com/Nearoo/pygame-text-input
[goats]: https://opengameart.org/content/mountain-goat-sprites
[font]: https://www.dafont.com/minecraft.font
[CC-BY]: https://creativecommons.org/licenses/by/4.0/
[CC-BY-NC-SA]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[MIT]: https://mit-license.org/
[GGJ]: https://globalgamejam.org/games/2024/3-2-5-can-you-count-2
[issue-129]: https://github.com/pygame-web/pygbag/issues/129
