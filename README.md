# one simple demo
#### 使用 Flask , apscheduler , subprocess
#### 達成類似 linux crontab 功能 (加上 python 產生的變數)

# 本次範例為定時取得指定地區天氣資料並寫 log 到 /tmp/taipei_weather.log
# 並寫兩隻 demo flask api
```
# curl sample
curl "http://127.0.0.1:8080/"
curl "http://127.0.0.1:8080/wttr?city=Tokyo"
curl "http://127.0.0.1:8080/bench_cpu?count=1000000000"
```

# linux 執行方法
export PYTHONPATH=/<project_path>/py_sh; /<py_path>/python3 /<project_path>/py_sh/app.py &

# linux add 開機自動執行
## add rc.local service (if not)
chmod +x /etc/rc.local
systemctl status rc-local.service
systemctl enable rc-local.service
systemctl start rc-local.service
systemctl status rc-local.service

## add rc.local 
vi /etc/rc.local
```
    export PYTHONPATH=/<project_path>/py_sh; /<py_path>/python3 /<project_path>/py_sh/app.py &
```
