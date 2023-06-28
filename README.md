<h1 align="center">Holograph Building Bridger</h1>

<h2>About the bot</h2>
Bot for bridging new holograph nft Building - https://app.holograph.xyz/ </br>


* Instruction and settings in config.py

* Private keys in  keys.txt </br>

* Need moralis api key - https://admin.moralis.io/settings#secret-keys
 </br>


<h2>Working modes</h2>

1. Bridge from a certain network to a certain network </br>
2. NFT search by networks and bridge to a random/selected network </br>



# Установка на Ubuntu
Обновляемся
```
sudo apt update && sudo apt upgrade -y
```
Скачиваем
```
git clone https://github.com/TatianaDEV7/BLDG-holo-bridger
```
Заходим в папку со скриптом
```
dir
cd BLDG-holo-bridger
```
Устанавливаем pip:
```
apt install python3-pip
pip install tqdm ccxt loguru termcolor telebot pyuseragents tabulate web3==6.4.0 pandas moralis
```
> На Ubuntu будет ругаться на библиотеку `pywin32==306`. Это нормально, она нужна только для Винды.
## Запуск (только после Настройки)
Настройка проходит в файле config.js, как написано выше нам для этого надо иметь api от [moralis](moralis.io), оставить mode = 0 для выбора сетей (без рандома), и вписать сети.
```bash
# Заходим в папку скрипта
cd /root/BLDG-holo-bridger

# Запуск с выводом stdout в командную строку
python3 main.py
# Запуск в фоновом режиме. Записывает логи в файл log.log
nohup python3 main.py > log.log 2>&1 &

# Завершить процесс:
pgrep -a python
kill (номер процесса)
```


<h2>donate</h2> evm 0xFD6594D11b13C6b1756E328cc13aC26742dBa868
<h2>donate</h2> trc20 TMmL915TX2CAPkh9SgF31U4Trr32NStRBp

<h2>тг</h2> https://t.me/iliocka
