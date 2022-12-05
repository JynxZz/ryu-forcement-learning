#--------------------------------------
# 						DEFAULT MAKE
#--------------------------------------
default: tree
##################### DEBUGGING HELPERS ####################
fbold=$(shell echo "\033[1m")
fnormal=$(shell echo "\033[0m")
ccgreen=$(shell echo "\033[0;32m")
ccblue=$(shell echo "\033[0;34m")
ccreset=$(shell echo "\033[0;39m")
############################################################

tree:
	@echo "\nHelp for the $(ccgreen)$(fbold)\`Ryu Forcement\` $(ccreset)$(fbold)\`Makefile\`$(ccreset)"

	@echo "\n$(ccgreen)$(fbold)SETUP ENV & PACKAGES$(ccreset)"

	@echo "\n        $(fbold)env$(ccreset)"
	@echo "            blablablabl."

	@echo "\n        $(fbold)install$(ccreset)"
	@echo "            blablablab."

	@echo "\n$(ccgreen)$(fbold)DIAMBRA$(ccreset)"

	@echo "\n        $(fbold)fight_classic$(ccreset)"
	@echo "            blablablab."
	@echo "\n        $(fbold)fight_raylib$(ccreset)"
	@echo "            blablablab."


#-------------------------------------
# 		  	SETUP ENV & PACKAGES
#--------------------------------------

env:
	@pyenv virtualenv 3.10.6 ryu-forcement-learning
	@pyenv local ryu-forcement-learning

install:
	@python3 -m pip install --upgrade pip
	@pip install -r requirements.txt

#--------------------------------------
# 		  				DIAMBRA
#--------------------------------------

gouki:
    while true; do diambra run python3 scripts/main.py gouki; done

ryu:
    while true; do diambra run python3 scripts/main.py ryu; done

ken:
    while true; do diambra run python3 scripts/main.py ken; done

osu:
    while true; do diambra run python3 scripts/main.py osu; done

fight_classic:
	@diambra run python3 scripts/main.py

fight_raylib:
	@diambra run python3 scripts/basic_raylib.py

#-------------------------------------
# 		 				BASH SCRIPT
#--------------------------------------

push:
	@sh dotfiles/.push.sh
