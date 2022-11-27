#!/bin/bash

if [ ! -d ~/code/ruy-forcement-learning ]; then
  mkdir ~/code/ruy-forcement-learning
fi

git clone git@github.com:JynxZz/ruy-forcement-learning.git ~/code/ruy-forcement-learning

echo 'alias rl="cd ~/code/ruy-forcement-learning"' >> ~/.aliases
echo '# Add Rom Path to DIAMBRA ARENA' >> ~/.zshrc
echo 'export DIAMBRAROMSPATH="$HOME/code/ruy-forcement-learning"' >> ~/.zshrc

cd ~/code/ruy-forcement-learning
make env 
make install

source ~/.zshrc
exec zsh 

echo 'I am ready to fight ...'
echo 'Start Training'
