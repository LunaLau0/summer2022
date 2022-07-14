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
