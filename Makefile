#--------------------------------------
# 						DEFAULT MAKE
#--------------------------------------
default: tree 

tree:
	@tree
	@echo 'Make list action: ' 

#-------------------------------------
# 		  	SETUP ENV & PACKAGE	
#--------------------------------------

env:
	@pyenv virtualenv 3.10.6 ruy-forcement-learning
	@pyenv local ruy-forcement-learning

path:
	@echo '# Add Path to the rom for DIAMBRA ARENA' >> ~/.zshrc
	@echo 'export DIAMBRAROMSPATH="{$HOME}/Developer/Perso/ruy-forcement-learning"' >> ~/.zshrc
	@source ~/.zshrc && exec zsh

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt 

#--------------------------------------
# 		  				DIAMBRA
#--------------------------------------

fight:
	@diambra run python script.py
