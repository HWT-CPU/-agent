-- 使用 root 用户执行此脚本，给 atagent 用户授权

-- 给 atagent 用户授予创建数据库的权限
GRANT CREATE ON *.* TO 'atagent'@'%';

-- 给 atagent 用户授予 dw 数据库的所有权限
GRANT ALL PRIVILEGES ON dw.* TO 'atagent'@'%';

-- 刷新权限
FLUSH PRIVILEGES;
