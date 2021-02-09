cd /home/jayjayjay/discord-bot/

git pull

pip freeze > temp.txt
pip uninstall -y -r temp.txt
rm temp.txt
pip install --no-cache-dir -r requirements.txt

python3 -m bot.42_bot
