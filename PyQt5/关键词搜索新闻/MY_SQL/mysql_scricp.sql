# 创建数据库.
-- CREATE database if NOT EXISTS news;
-- use news;

# 创建数据表.
CREATE TABLE if NOT EXISTS words(
  id INT PRIMARY KEY auto_increment COMMENT 'ID',
  keyword VARCHAR(20) COMMENT '关键词',
  new_url VARCHAR(8182) COMMENT '新闻url',
  new_tag VARCHAR(200) COMMENT '新闻来源发布时间',
  new_summary text COMMENT '新闻内容',
  source VARCHAR(20) COMMENT '获取平台',
  create_time  TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  update_time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
 ) auto_increment=1;

select * from words;



