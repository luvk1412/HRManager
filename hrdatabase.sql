-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: hrmanager
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `attendance` (
  `date` date DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  KEY `id` (`id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES ('2018-03-28',2),('2018-03-28',1),('2018-03-31',1),('2018-04-02',1),('2018-04-02',2),('2018-04-02',3),('2018-04-02',4),('2018-04-02',5),('2018-04-02',7),('2018-04-02',8);
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city_state`
--

DROP TABLE IF EXISTS `city_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city_state` (
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `pincode` int(11) NOT NULL,
  PRIMARY KEY (`pincode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city_state`
--

LOCK TABLES `city_state` WRITE;
/*!40000 ALTER TABLE `city_state` DISABLE KEYS */;
INSERT INTO `city_state` VALUES ('Roorkie','Haryana',120124),('BIhar','Uttar Pradesh',134701),('Amritsar','Punjab',143001),('Allahabad','Uttar Pradesh',211012);
/*!40000 ALTER TABLE `city_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `e_v`
--

DROP TABLE IF EXISTS `e_v`;
/*!50001 DROP VIEW IF EXISTS `e_v`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `e_v` AS SELECT 
 1 AS `id`,
 1 AS `name`,
 1 AS `email`,
 1 AS `department`,
 1 AS `designation`,
 1 AS `address`,
 1 AS `contact`,
 1 AS `password`,
 1 AS `reg_date`,
 1 AS `admin`,
 1 AS `pincode`,
 1 AS `gender`,
 1 AS `dob`,
 1 AS `state`,
 1 AS `city`,
 1 AS `nationality`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employee` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `reg_date` date DEFAULT NULL,
  `admin` int(11) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Luv','luvk1412@gmail.com','Overall','Ceo','BH$ IIIT Allahabad','9803674332','$5$rounds=535000$38RGBfeJwjjpm6B7$yWfNa4RS/GG5cMTF9PBjxjOnlLy/i71g7h5fKtIdBc2','2018-03-26',1,'143001','male','1997-12-14'),(2,'Luv not admin','luvk1412@gmail.com','Overall','Ceo','1246/1 opposite Tari Halwai, Katra Baghian, Amritsar','9803674332','$5$rounds=535000$JpDXXavvF3k24dlP$hiJh0TZXzLsrpXR0JjxC.M7MFCwbMIHpRGC1JDheTp7','2018-03-27',1,'143001','male','1997-12-14'),(3,'mradul','iim2016005@iiita.ac.in','Finance','HOD','IIITA','7607020702','$5$rounds=535000$WSOuV0FfmlQzH/.3$R5WYOeL2leJ8uNB/DteuZBJhGQIB/NTDqZbiHGav.77','2018-03-29',0,'211012','male','1997-02-18'),(4,'Parag Parihar','trdrdrtdr@gmail.com','Overall','Peon','ghar','9587629647','$5$rounds=535000$.b6.vVZZ6CnLAsvQ$/6tTx2U8tEUU.1CnUV3xMq8K6JGTl3sn3F/3GJZj4q8','2018-03-29',0,'211012','male','2018-03-10'),(5,'Lakshya Khattar','iit2016009@iiita.ac.in','Overall','Ceo','221B-Baker Street','9888330112','$5$rounds=535000$DpxISBcrU745nm7B$OntA/V.oVFsMRjzg..i/qGwwVknXM3z78QTr1wgcfc0','2018-04-01',0,'143001','male','1998-07-17'),(7,'Haresh','haresh@gmailcom','Sales','Employee','IITR','856975552','$5$rounds=535000$Y/4aRbEYnkhcsnAJ$TtIV7yuoMKvsm6.xlKwSLXOCE7.RQ5lkilcZu0RKUl7','2018-04-02',0,'120124','male','1997-01-31'),(8,'Amit','amlkfnafln','Sales','Employee','kfnsdkjanfkjngkj','8985926','$5$rounds=535000$j12Niq8cB6aVsik1$TG4c35Bt29ET3KuwcgFuD5pwEFJDv7rRZ3q4RnYfwV8','2018-04-02',0,'211012','male','1997-12-31'),(9,'Rani','Rani@gmail.com','Finance','Intern','1234 streer','9803457982','$5$rounds=535000$CJ6WbFfpHrqyA2TV$K.a/DI//86e1GVO5.A4jsbiu8CkKtqoTeOeQeRHulq1','2018-04-02',0,'211012','female','1996-12-12'),(10,'Lakshmi','lakshmi@gmail.com','Research','Manager','Lakshmi Street','9803674552','$5$rounds=535000$ClhE90v/hxm6xHLL$3/lgQEA5c9YMu0BqBOIJU1vhzcSI4M3pHptB5pXD4K2','2018-04-02',0,'134701','female','1997-05-17');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incentive`
--

DROP TABLE IF EXISTS `incentive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incentive` (
  `date` date DEFAULT NULL,
  `hours` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  KEY `id` (`id`),
  CONSTRAINT `incentive_ibfk_1` FOREIGN KEY (`id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incentive`
--

LOCK TABLES `incentive` WRITE;
/*!40000 ALTER TABLE `incentive` DISABLE KEYS */;
INSERT INTO `incentive` VALUES ('2018-03-28',2,1),('2018-03-28',12,2);
/*!40000 ALTER TABLE `incentive` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salary`
--

DROP TABLE IF EXISTS `salary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `salary` (
  `department` varchar(50) DEFAULT NULL,
  `designation` varchar(50) DEFAULT NULL,
  `amount_per_hour` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salary`
--

LOCK TABLES `salary` WRITE;
/*!40000 ALTER TABLE `salary` DISABLE KEYS */;
INSERT INTO `salary` VALUES ('Overall','Ceo',2000),('Overall','Peon',50),('Finance','HOD',1500),('Finance','Manager',1000),('Finance','Employee',600),('Finance','Intern',150),('Research','HOD',1500),('Research','Manager',1000),('Research','Employee',600),('Research','Intern',150),('Sales','HOD',1500),('Sales','Manager',1000),('Sales','Employee',600),('Sales','Intern',150),('Marketing','HOD',1500),('Marketing','Manager',1000),('Marketing','Employee',600),('Marketing','Intern',1);
/*!40000 ALTER TABLE `salary` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `state_nationality`
--

DROP TABLE IF EXISTS `state_nationality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `state_nationality` (
  `state` varchar(100) NOT NULL,
  `nationality` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `state_nationality`
--

LOCK TABLES `state_nationality` WRITE;
/*!40000 ALTER TABLE `state_nationality` DISABLE KEYS */;
INSERT INTO `state_nationality` VALUES ('Haryana','Indian'),('Punjab','Indian'),('Uttar Pradesh','Indian');
/*!40000 ALTER TABLE `state_nationality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `e_v`
--

/*!50001 DROP VIEW IF EXISTS `e_v`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `e_v` AS select `e`.`id` AS `id`,`e`.`name` AS `name`,`e`.`email` AS `email`,`e`.`department` AS `department`,`e`.`designation` AS `designation`,`e`.`address` AS `address`,`e`.`contact` AS `contact`,`e`.`password` AS `password`,`e`.`reg_date` AS `reg_date`,`e`.`admin` AS `admin`,`e`.`pincode` AS `pincode`,`e`.`gender` AS `gender`,`e`.`dob` AS `dob`,`cs`.`state` AS `state`,`cs`.`city` AS `city`,`sn`.`nationality` AS `nationality` from ((`employee` `e` join `city_state` `cs`) join `state_nationality` `sn`) where ((`e`.`pincode` = `cs`.`pincode`) and (`cs`.`state` = `sn`.`state`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-16 19:55:10
