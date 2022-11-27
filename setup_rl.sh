#!/bin/bash

if [ ! -d ~/code/project]; then
  mkdir ~/code/project
fi

git clone git@github.com:JynxZz/ruy-forcement-learning.git ~/code/project

echo 'alias rl="cd ~/code/project/ruy-forcement-learning"' >> ~/.aliases
echo '# Add Rom Path to DIAMBRA ARENA' >> ~/.zshrc
echo 'export DIAMBRAROMSPATH="$HOME/code/ruy-forcement-learning"' >> ~/.zshrc

cd ~/code/project/ruy-forcement-learning
make env 
make install

source ~/.zshrc
exec zsh 

echo 'I am ready to fight ...'
echo 'Start Training'
