## Monarch
[![Build Status](https://travis-ci.com/xiezg247/Monarch.svg?branch=master)](https://travis-ci.com/xiezg247/Monarch)
## 项目介绍
测试项目

## 规范
- [开发规范](doc/开发规范.md)
- [提交规范](doc/Git提交规范.md)
- [API设计](doc/API设计.md)
- [敏捷开发](https://xiezg247.xyz/2017/12/07/敏捷开发模式下的项目复盘/)

## 项目运行
### 创建数据库
```python
CREATE DATABASE `monarch` /*!40100 COLLATE 'utf8mb4_general_ci' */;
```

### 创建/更新数据表
```python
python manage.py db revision -m "create user table"
python manage.py db upgrade
```

### 启动程序(单进程模式)
```python
python manage.py runserver -h 0.0.0.0 -p 5000
```

### 启动程序(gevent模式)
```python
gunicorn -k gevent -t 10 -w 4 -b "0.0.0.0:8015" monarch.wsgi:application
```
或
```python
gunicorn -c gunicorn_config.py monarch.wsgi:application
```

### 启动celery worker
```python
celery worker -A manage.celery --loglevel=INFO -c 4 -P gevent -Q celery
```

### 启动celery beat
```python
celery beat -A monarch.celery --loglevel=INFO
```
