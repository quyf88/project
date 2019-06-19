# 创建数据库.
-- CREATE database if NOT EXISTS news;
-- use news;

# 创建数据表.
CREATE TABLE if NOT EXISTS words(
  id INT PRIMARY KEY auto_increment COMMENT 'ID',
  symbol VARCHAR(20) COMMENT '股票代码',
  nam VARCHAR(20) COMMENT '名称',
  trade VARCHAR(20) COMMENT '最新价',
  pricechange VARCHAR(20) COMMENT '涨跌额',
  changepercent VARCHAR(20) COMMENT '涨跌幅',
  buy VARCHAR(20) COMMENT '买入',
  sell VARCHAR(20) COMMENT '卖出',
  settlement VARCHAR(20) COMMENT '昨收',
  opens VARCHAR(20) COMMENT '今开',
  high VARCHAR(20) COMMENT '最高',
  low VARCHAR(20) COMMENT '最低',
  volume VARCHAR(20) COMMENT '成交量',
  amount VARCHAR(20) COMMENT '成交额',
  create_time  TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
 ) auto_increment=1;

select * from words;



