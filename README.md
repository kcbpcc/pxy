python 3.9 - https://www.python.org/downloads/release/python-390/

Git - https://git-scm.com/downloads

sudo timedatectl set-timezone UTC && sudo timedatectl set-local-rtc 0 && timedatectl

sudo usermod -aG sudo pxy

sudo usermod -aG sudo userland

sudo apt update

sudo apt install software-properties-common

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt update

sudo apt install python3.9

python3.9 --version

sudo apt install python3.9-venv

python3.9 -m venv env

source ~/env/bin/activate

pip install --upgrade pip

sudo apt install git

git --version

git clone https://github.com/kcbpcc/pxy.git

sudo cp ~/pxy/sys/pxy* /usr/local/bin/

sudo chmod +x /usr/local/bin/pxy*

cd ~/pxy/sys/exe

pip install -r requirements.txt

cd ~/pxy/sys/exe/run



