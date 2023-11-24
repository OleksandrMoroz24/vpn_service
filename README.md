# VPN test task
## Setting up the environment:

Python3 must be already installed

Windows
```shell
git clone https://github.com/OleksandrMoroz24/vpn_service
cd vpn_service
python -m venv venv
.\\venv\\Scripts\\activate
pip install -r requirements.txt
docker pull oleksandrmoroz24/vpn-service
docker run -d -p 8000:8000 oleksandrmoroz24/vpn-service
```

MacOS
```shell
git clone https://github.com/OleksandrMoroz24/vpn_service
cd vpn_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker pull oleksandrmoroz24/vpn-service
docker run -d -p 8000:8000 oleksandrmoroz24/vpn-service
```