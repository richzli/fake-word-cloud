# fake-word-cloud

it's a word cloud, with fake words and fun physics

you need PyOpenGL installed; it only worked for me (windows) after i used the wheels [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl), install both PyOpenGL and PyOpenGL_accelerate, as well as freetype-py

if you are on windows like me (again) you probably also need the freetype dlls, found [here](https://github.com/ubawurinna/freetype-windows-binaries); just drop it anywhere in your PATH (straight in this directory works too)

also you can take any font and put it in `./font.ttf`

## description

generates fake words using a simple markov chain

data compiled using words length 6 or greater from 5000 random wikipedia articles; train data yourself by editing and running `data/train.py`

displays these fake words prettily using a simple custom physics engine (wip)

## usage

`python main.py`