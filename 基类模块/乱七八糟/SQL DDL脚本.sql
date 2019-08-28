/*==============================================================*/
/* 股票信息数据库DDL脚本                                        */
/*==============================================================*/

/* 创建数据库 */
create database if not exists pufabank;

use pufabank;

drop table if exists HistoricalQuote;    /* 历史数据表 */

drop table if exists Fixed;              /* 固定参数表 */

/*==============================================================*/
/* Table: HistoricalQuote                                       */
/*==============================================================*/
create table HistoricalQuote
(
	Id                  int(255) not null ,     /* 关键词id自动递增 */
   Sname				varchar(10) not null,	/* 名字 */
   Hfqjg                decimal(20,8) not null,	/*     */
   Tdate                date not null,			/* 交易日期 */
   Close                decimal(8,2),			/* 收盘价（元）*/
   Zdf                  decimal(8,4),		    /* 1天跌涨幅度（%）*/
   Zdf3                 decimal(20,16),		    /* 3天跌涨幅度（%）*/
   Zdf5                 decimal(20,16),		    /* 5天跌涨幅度（%）*/
   Zdf10                decimal(20,16),		    /* 10天跌涨幅度（%）*/
   AGSZBHXS             decimal(15,2),
/*==============================================================*/
/*                         融资                                 */
/*==============================================================*/		                      
   Rzye                 decimal(15,2),		    /* 余额（元）*/
   Rzyezb               decimal(5,2),		    /* 余额占流通市值比（%）*/
   Rzmre                decimal(10,2),		    /* 1天买入额（元）*/
   Rzmre3               decimal(10,2),		    /* 3天买入额（元）*/
   Rzmre5               decimal(10,2),		    /* 5天买入额（元）*/
   Rzmre10              decimal(10,2),		    /* 10天买入额（元）*/
   Rzche                decimal(10,2),		    /* 1天偿还额（元）*/
   Rzche3               decimal(10,2),		    /* 3天偿还额（元）*/
   Rzche5               decimal(10,2),		    /* 5天偿还额（元）*/
   Rzche10              decimal(10,2),		    /* 10天偿还额（元）*/
   Rzjmre               decimal(10,2),		    /* 1天净买入（元）*/
   Rzjmre3              decimal(10,2),		    /* 3天净买入（元）*/
   Rzjmre5              decimal(10,2),		    /* 5天净买入（元）*/
   Rzjmre10             decimal(10,2),		    /* 10天净买入（元）*/
/*==============================================================*/
/*                         融券                                 */
/*==============================================================*/	
   Rqye                 decimal(10,2),		    /* 余额（元） */
   Rqyl                 decimal(10,2),		    /* 余量（股）*/
   Rqmcl                decimal(8,2),		    /* 1天卖出量（股）*/
   Rqmcl3               decimal(8,2),		    /* 3天卖出量（股）*/
   Rqmcl5               decimal(8,2),		    /* 5天卖出量（股）*/
   Rqmcl10              decimal(8,2),		    /* 10天卖出量（股）*/
   Rqchl                decimal(8,2),		    /* 1天偿还量（股）*/
   Rqchl3               decimal(8,2),		    /* 3天偿还量（股）*/
   Rqchl5               decimal(8,2),		    /* 5天偿还量（股）*/
   Rqchl10              decimal(8,2),		    /* 10天偿还量（股）*/
   Rqjmcl               decimal(8,2),		    /* 1天净卖出（股）*/
   Rqjmcl3              decimal(8,2),		    /* 3天净卖出（股）*/
   Rqjmcl5              decimal(8,2),		    /* 5天净卖出（股）*/
   Rqjmcl10             decimal(8,2),		    /* 10天净卖出（股）*/
   
   Rzrqye               decimal(15,2),		    /* 融资融券余额（元）*/
   Rzrqyec              decimal(15,2),		    /* 融资融券余额差值（元）*/   
   WriteDate           datetime not null DEFAULT NOW(),    /* 写入时间 */
   primary key (Id)   
);


/*==============================================================*/
/* Table: Fixed                                                 */
/*==============================================================*/
create table Fixed
(
    Scode               bigint not null,  					/* 代码 */
	Sname				varchar(10) not null,				/* 名字 */
	Market				varchar(10) not null,				/* 市场 */
	WriteDate           datetime not null DEFAULT NOW(),    /* 写入时间 */

   primary key (Scode)
);

/* 设置关联表 */

/* alter table HistoricalQuote add constraint FK_ID foreign key (Sname)
      references Fixed (Sname) on delete restrict on update restrict; */

/* alter table 从表 add constraint 外键（形如：FK_从表_主表） foreign key (从表外键字段) references 主表(主键字段);	*/
	  

/* 插入数据 */
insert into Fixed (Scode, Sname, Market) values ('600000', '浦发银行', 'SH');

