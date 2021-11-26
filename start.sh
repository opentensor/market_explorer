python3 pull.py
python3 query.py

pm2 start pull.py --name pull --interpreter python3  --cron "*/15 * * * *"
pm2 start query.py --name query --interpreter python3 --cron "*/15 * * * *"
pm2 start serve.py --name serve --interpreter python3 

