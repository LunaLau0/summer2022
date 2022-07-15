# 开始运行mysql server
sudo systemctl start mysql.service  
通过以下命令来检查MySQL服务器是否启动：  
ps -ef | grep mysqld  
如果MySql已经启动，以上命令将输出mysql进程列表:
```
mysql     4472     1  0 Jul12 ?        00:00:18 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid
luna     26504 26491  0 13:01 pts/0    00:00:00 grep --color=auto mysqld
```

## mysql用户创建、权限管理
CREATE user 'guest'@'%' identified by 'password'  
GRANT SELECT ON *.* TO 'guest'@'%'; 

## upload my local sql files to the service
scp /path/filename username@servername:/path   
例如scp /var/www/test.php  root@192.168.0.101:/var/www/  
把本机/var/www/目录下的test.php文件上传到192.168.0.101这台服务器上的/var/www/目录中

在命令的最后添加一个'&',表示在后台运行，通过'ps'与进程id(四位数字)查询是否持续运行
scp /Users/luna/Downloads/yd.zip luna@124.71.156.199:/home/luna/sql_files &

sudo apt-get install unzip  
unzip sql_files

mysql -u username -p database_name < file.sql

mysql -u root -p yd < /home/luna/yd/217.sql
mysql -u root -p yd < /home/luna/yd/218.sql


mysql -u root yd < /home/luna/yd/device.sql
mysql -u root yd < /home/luna/yd/electricts.sql
mysql -u root yd < /home/luna/yd/unit.sql
mysql -u root yd < /home/luna/yd/unitdevice.sql
mysql -u root yd < /home/luna/yd/device.sql


# 本地配置mysql环境，完成数据重构编辑
brew install mysql  
```
(base) ➜  ~ mysql -v
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)
```
该报错源于:  
You'll need to start MySQL before you can use the  ```mysql``` command on your terminal. To do this, run ```brew services start mysql```. By default, brew installs the MySQL database without a root password.  
brew services start mysql  
mysql -uroot  
