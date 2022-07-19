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
brew services stop mysql
brew services restart mysql  

在本地mysql导入数据：  
```
mysql -u root yd < /Users/luna/Downloads/yd/device.sql
mysql -u root yd < /Users/luna/Downloads/yd/electricts.sql
mysql -u root yd < /Users/luna/Downloads/yd/unit.sql
mysql -u root yd < /Users/luna/Downloads/yd/unitdevice.sql
mysql -u root yd < /Users/luna/Downloads/yd/device.sql
```

由于本地使用code打开226.sql时反复报错，更改使用remote vim来replace sql file context  


# remote edit/replace <table_name> in files, and read into mysql
## vim replace方法

```:%s/<table_name>/electricts227/g```  
把该文件中所有的<table_name>更换为electricts227


For example, if we want to rename example1.txt into example2.txt, we would use:  
mv example1.txt example2.txt

确认原文档内容：  
1. electrics.sql是表格结构，CREATE TABLE `electricts226`   
2. 226.sql只包含数据，不包含注释，从头至尾只有INSERT INTO ...
3. query -> ^c直接查看行数，与#.sql行数一致，即表示数据导入完成

由于读取数据后发现行数对应不上，应该是没读完就卡死了，所以drop table重新导入  
drop table electrics226;  
cd ../home/luna/yd  
mv electrics.sql electrics226.sql  
为了对后续electric表格进行区分（复制12个表格结构后），把原来的electrics.sql重命名为electrics226.sql  

mysql -u root yd < /home/luna/yd/electricts226.sql  

## 复制elec226表格结构  
CREATE TABLE electricts217 LIKE electricts226;  
create table electricts219 like electricts226;

1. 217 990378 lines
2. 218 1042804 lines
3. 219 1024534 lines
4. 2110 1156140 lines
5. 2111 1146799 lines
6. 2112 1249983 lines
7. 221 1255691 lines
8. 222 1130067 lines
9. 223 1227214
10. 224 1067753
11. 225 1236300
12. 227 226837  

根据观察，平均每个sql分表需要20-30分钟读取，因此可以使用screen命令来运行，减少需要手动在窗口前等待的时间  
```
mysql -u root yd < /home/luna/yd/223.sql
mysql -u root yd < /home/luna/yd/224.sql
mysql -u root yd < /home/luna/yd/225.sql
mysql -u root yd < /home/luna/yd/227.sql
```

**以上，对mysql中yd数据的搭建全部完成，接下来赋予guest访问权限，赋予luna等价root的权限**  
参考链接为：  
<https://www.cnblogs.com/richardzhu/p/3318595.html>

# 用python的Django搭建一个获取数据的API
use ```pip3``` instead of ```pip```, although all the instrucutons said "pip"  

