# Setup Virtual Machine

---

## First Step

```bash
sudo apt-get update && sudo apt-get upgrade
```

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
```

### Change theme

```bash
vim ~/.bashrc
```

Change the font theme to the _agnoster_ theme.

## Install Pyenv & Pyenv Virtual

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
```

Running this following to add pyenv to the profile

```bash
cat << EOF >> ~/.profile
export PYENV_ROOT="\$HOME/.pyenv"
export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init --path)"
EOF
```

### Adding plugin to the bashrc

```bash
vim ~/.bashrc
```

Add pyenv to the list of bash plugins on the line with plugins=(git) in ~/.bashrc: in the end, you should have plugins=(git pyenv)

---

## Installing Python

```bash
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
python3-dev
```

```bash
sudo apt-get install python3-pip -y
```

When finish, exit oh-my-bash and the VM (exit twice) and reconnecto the VM.

```bash
exit
exit
gcloud compute ssh $INSTANCE_NAME
```

## Installing Docker

Dependencies first

```bash
sudo apt install apt-transport-https curl gnupg-agent ca-certificates software-properties-common -y
```

The key

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

The repo

```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

Install

```bash
sudo apt install docker-ce docker-ce-cli containerd.io -y
```

Give acces to sudo

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Don't forget to clean

```bash
clean
exec bash
```

## Give ssh agent

Give SSH acces to the repo git
This commande line not in the VM

```bash
gcloud compute scp ~/.ssh/id_ed25519 $INSTANCE_NAME:~/.ssh/
```

Then, inside the VM you can allow acces to the repo git ssh acces

```bash
ssh-add ~/.ssh/id_ed25519
```

Give the passphrase Git

## Install Dependencies to run the game

_ffmpeg libsm6 libxext6 tkinter_

```bash
sudo apt-get install ffmpeg libsm6 libxext6 python3-tk make -y && exec bash
```

To be sure, reset VM before the next step.

---

# Ryu Forcement Learning

```bash
curl https://raw.githubusercontent.com/JynxZz/ryu-forcement-learning/master/dotfiles/.setup_rl.sh | sh && exec zsh
```

Make sure the repo is on the good path
Then run this commands to set up the env & the install of package python

```bash
cd ~/code/ryu-forcement-learning/
make env && make install
```

---

# TODO : modif makefile fight (python3)

# TODO : modif script bash ton write path in good files (alias don't exist on bash, write everything inside ~/.bashrc)

---
