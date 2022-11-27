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

fight:
	@diambra run python script.py


#-------------------------------------
# 		 				KEEP PUSHING 
#--------------------------------------

push:
	@sh dotfiles/.push.sh
	
