#--------------------------------------
# 						DEFAULT MAKE
#--------------------------------------
default: tree 

tree:
	@echo 'Go Train ... !!'
	@echo 'make env - to setup up virtual env '
	@echo 'make install - to install packages & dependances'
	@echo 'make fight - to fight !!'


#-------------------------------------
# 		  	SETUP ENV & PACKAGE	
#--------------------------------------

env:
	@pyenv virtualenv 3.10.6 ryu-forcement-learning
	@pyenv local ryu-forcement-learning

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt 

#--------------------------------------
# 		  				DIAMBRA
#--------------------------------------

fight_classic:
	@diambra run python scripts/script.py

fight_raylib:
	@diambra run python scripts/basic_raylib.py


#-------------------------------------
# 		 				KEEP PUSHING 
#--------------------------------------

push:
	@sh dotfiles/.push.sh
	
