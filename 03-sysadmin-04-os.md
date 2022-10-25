##1. 
Скачиваем программу
wget https://github.com/prometheus/node_exporter/releases/download/v1.4.0/node_exporter-1.4.0.linux-amd64.tar.gz
Распаковываем 
tar zxvf node_exporter-1.4.0.linux-amd64.tar.gz 
Копируем исполняемый файл в общедоступную папку
sudo cp node_exporter-1.4.0.linux-amd64/node_exporter /usr/local/bin/
Создаем файл для unit
    sudo systemctl edit --force --full node_exporter.service
с содержимым
[Unit]

Description=Node_exporter daemon
After=syslog.target network.target

[Service]

ExecStart=/usr/local/bin/node_exporter
Restart=on-failure

[Install]
WantedBy=multi-user.target

Перечитываем конфигурационные файлы systemd
sudo systemctl daemon-reload 
Создаем линк
sudo systemctl enable node_exporter.service
Стартуем сервис 
sudo systemctl start node_exporter.service
Смотрим стататус
```
sudo systemctl status node_exporter.service
● node_exporter.service - Node_exporter daemon
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-10-25 11:56:14 MSK; 39s ago
   Main PID: 1673 (node_exporter)
      Tasks: 4 (limit: 9484)
     Memory: 2.3M
     CGroup: /system.slice/node_exporter.service
             └─1673 /usr/local/bin/node_exporter
```
Если все ок, перегружаем VM поверям еще раз.
```
● node_exporter.service - Node_exporter daemon
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2022-10-25 11:58:35 MSK; 1min 37s ago
   Main PID: 707 (node_exporter)
      Tasks: 5 (limit: 9484)
     Memory: 14.1M
     CGroup: /system.slice/node_exporter.service
             └─707 /usr/local/bin/node_exporter
```
---
##2.
Получаем от node_exporter информацию от свободном дисковом пространстве 
    curl localhost:9100/metrics 2>/dev/null |grep node_filesystem_free_bytes

Получаем информацию об ошибках netstat
    curl localhost:9100/metrics 2>/dev/null |grep netstat |grep Errors

Нагрузка на память
    curl localhost:9100/metrics 2>/dev/null |grep pressure_memory

Нагрузку на процессор в разрезе ядер
    curl localhost:9100/metrics 2>/dev/null |grep node_cpu_seconds_total

---
##3.
