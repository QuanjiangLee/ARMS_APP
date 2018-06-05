-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ttt
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `serviceApp_carparts`
--

DROP TABLE IF EXISTS `serviceApp_carparts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serviceApp_carparts` (
  `partId` int(11) NOT NULL AUTO_INCREMENT,
  `partName` varchar(40) NOT NULL,
  `partNumber` int(11) NOT NULL,
  `partPrice` double NOT NULL,
  `partDate` datetime(6) NOT NULL,
  PRIMARY KEY (`partId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serviceApp_carparts`
--

LOCK TABLES `serviceApp_carparts` WRITE;
/*!40000 ALTER TABLE `serviceApp_carparts` DISABLE KEYS */;
/*!40000 ALTER TABLE `serviceApp_carparts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serviceApp_repairinfo`
--

DROP TABLE IF EXISTS `serviceApp_repairinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serviceApp_repairinfo` (
  `repairId` int(11) NOT NULL AUTO_INCREMENT,
  `repair_fault` varchar(255) NOT NULL,
  `repair_carName` varchar(40) NOT NULL,
  `repair_carNum` varchar(40) NOT NULL,
  `repair_carPhone` varchar(40) NOT NULL,
  `repair_status` tinyint(1) NOT NULL,
  `repairDetails` varchar(255) NOT NULL,
  `partDetails` varchar(255) NOT NULL,
  `totalPrice` double NOT NULL,
  `repairingDate` varchar(40) NOT NULL,
  `repairdDate` varchar(40) NOT NULL,
  `personId_id` int(11) NOT NULL,
  `repairMask` varchar(255) NOT NULL,
  PRIMARY KEY (`repairId`),
  KEY `personId_id` (`personId_id`),
  CONSTRAINT `serviceApp_repairinfo_ibfk_1` FOREIGN KEY (`personId_id`) REFERENCES `serviceApp_userinf` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serviceApp_repairinfo`
--

LOCK TABLES `serviceApp_repairinfo` WRITE;
/*!40000 ALTER TABLE `serviceApp_repairinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `serviceApp_repairinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serviceApp_userinf`
--

DROP TABLE IF EXISTS `serviceApp_userinf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serviceApp_userinf` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(30) NOT NULL,
  `user_nickname` varchar(30) NOT NULL,
  `user_grant` tinyint(1) NOT NULL,
  `user_sex` varchar(5) NOT NULL,
  `user_mask` varchar(100) NOT NULL,
  `user_passwd` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serviceApp_userinf`
--

LOCK TABLES `serviceApp_userinf` WRITE;
/*!40000 ALTER TABLE `serviceApp_userinf` DISABLE KEYS */;
INSERT INTO `serviceApp_userinf` VALUES (1,'admin','管理员',1,'男','这个人太懒了！','*4ACFE3202A5FF5CF467898FC58AAB1D615029441'),(2,'worker','维修工',0,'男','这个人太懒了！','*33D57FB5547E9D2810E3BF7CE07BEE9482CB78BF'),(3,'test','维修工',0,'男','这个人太懒了！','*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29'),(4,'admin2','管理员',1,'男','这个人太懒了！','*0E6FD44C7B722784DAE6E67EF8C06FB1ACB3E0A6');
/*!40000 ALTER TABLE `serviceApp_userinf` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-06  0:30:21
