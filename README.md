# fake-word-cloud

it's a word cloud, with fake words and fun physics

you need PyOpenGL installed; it only worked after i used the wheels [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl), install both PyOpenGL and PyOpenGL_accelerate

## description

generates fake words using a simple markov chain

data compiled using words length 6 or greater from 5000 random wikipedia articles; train data yourself by editing and running `data/train.py`

displays these fake words prettily using a custom physics engine (wip)

## usage

`python main.py`