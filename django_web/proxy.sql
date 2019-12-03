/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 80018
Source Host           : localhost:3306
Source Database       : proxy

Target Server Type    : MYSQL
Target Server Version : 80018
File Encoding         : 65001

Date: 2019-12-03 15:00:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for alipay
-- ----------------------------
DROP TABLE IF EXISTS `alipay`;
CREATE TABLE `alipay` (
  `ID` varchar(255) NOT NULL COMMENT 'UUID',
  `LongUrl` varchar(10000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '长链接',
  `ShortLink` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '短链接',
  `Udeta` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `Datatime` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of alipay
-- ----------------------------
INSERT INTO `alipay` VALUES ('872dc84414ca11ea9aec28d2447ab52e', 'https://ds.alipay.com/?from=mobilecodec&scheme=alipays%3A%2F%2Fplatformapi%2Fstartapp%3FappId%3D20000200%26actionType%3DtoCard%26sourceId=bill%26cardNo=6215581504002740252%26bankAccount=%E5%BC%A0%E5%B0%8F%E5%8D%8E%0A%26money=%26amount=%26bankMark=ICBC%26bankName=%E5%B7%A5%E5%95%86%E9%93%B6%E8%A1%8C%26cardNoHidden=true%26cardChannel=HISTORY_CARD%26orderSource=from', 'https://dwz.cn/UDLUb5qk', '2019-12-02 14:31:53', '2019-12-02 14:31:53');

-- ----------------------------
-- Table structure for anti-fraud
-- ----------------------------
DROP TABLE IF EXISTS `anti-fraud`;
CREATE TABLE `anti-fraud` (
  `ID` varchar(255) NOT NULL,
  `Business` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '业务名称',
  `Expiration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '' COMMENT '账号有效期',
  `Status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'True' COMMENT '状态：True有效期内',
  `Udeta` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `Datatime` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of anti-fraud
-- ----------------------------
INSERT INTO `anti-fraud` VALUES ('460a23180f3411ea9aec28d2447ab52e', '测试', '一个月', 'True', '2019-12-02 13:40:52', '2019-11-14 14:25:02');
