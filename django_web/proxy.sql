/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 80018
Source Host           : localhost:3306
Source Database       : proxy

Target Server Type    : MYSQL
Target Server Version : 80018
File Encoding         : 65001

Date: 2019-11-25 17:47:18
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for anti-fraud
-- ----------------------------
DROP TABLE IF EXISTS `anti-fraud`;
CREATE TABLE `anti-fraud` (
  `ID` varchar(255) NOT NULL,
  `Business` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '业务',
  `Status` enum('True','Flase') DEFAULT 'True' COMMENT '状态：True有效期内',
  `Datatime` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of anti-fraud
-- ----------------------------
INSERT INTO `anti-fraud` VALUES ('460a23180f3411ea9aec28d2447ab52e', '测试', 'True', '2019-11-25 11:22:59');
