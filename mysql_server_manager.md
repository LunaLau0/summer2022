## 开始运行mysql server
sudo systemctl start mysql.service

### mysql用户创建、权限管理
CREATE user 'luna'@'%' identified by 'password'
GRANT ALL ON *.* TO 'luna'@'%'; 