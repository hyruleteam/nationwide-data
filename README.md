# 全国各省市区数据获取

核心是一个python脚本，会生成一个`data.json`文件。`example`中的示例是各语言实现将数据导入到数据库的实现，可以自定义自行编写。

## 脚本说明

* 进入`core`文件夹，执行`pip install -r requirements.txt`安装依赖
* 安装完成之后，执行python geo.py (要求python3.5+)

## 当前表结构

| 字段名 | 类型 | 长度 |
| ------ | ------ | ------ |
| id | CHAR | 36 |
| pid | CHAR | 36 |
| name | VARCHAR | 50 |
| code | VARCHAR | 50 |