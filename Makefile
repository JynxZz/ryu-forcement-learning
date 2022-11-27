#--------------------------------------
# 						DEFAULT MAKE
#--------------------------------------
default: tree 

tree:
	@tree
	@echo 'Go Train ... !!'

#-------------------------------------
# 		  	SETUP ENV & PACKAGE	
#--------------------------------------

env:
	@pyenv virtualenv 3.10.6 ruy-forcement-learning
	@pyenv local ruy-forcement-learning

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt 

#--------------------------------------
# 		  				DIAMBRA
#--------------------------------------

fight:
	@diambra run python script.py
