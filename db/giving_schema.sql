-- MySQL dump 10.13  Distrib 5.5.31, for Linux (x86_64)
--
-- Host: givingdb.c5faqozfo86k.us-west-2.rds.amazonaws.com    Database: giving
-- ------------------------------------------------------
-- Server version	5.5.31-log

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
-- Table structure for table `causes`
--

DROP TABLE IF EXISTS `causes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `causes` (
  `causes_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `alias1` varchar(100) DEFAULT NULL,
  `alias2` varchar(100) DEFAULT NULL,
  `alias3` varchar(100) DEFAULT NULL,
  `alias4` varchar(100) DEFAULT NULL,
  `alias5` varchar(100) DEFAULT NULL,
  `alias6` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`causes_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1307 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `causes_nonprofits_rel`
--

DROP TABLE IF EXISTS `causes_nonprofits_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `causes_nonprofits_rel` (
  `causes_nonprofits_rel_id` int(10) NOT NULL AUTO_INCREMENT,
  `causes_id` int(11) NOT NULL,
  `nonprofits_id` int(11) NOT NULL,
  PRIMARY KEY (`causes_nonprofits_rel_id`),
  KEY `cause_id_idx` (`causes_id`),
  KEY `nonprofit_id_idx` (`nonprofits_id`)
) ENGINE=InnoDB AUTO_INCREMENT=42303 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `causes_nonprofits_rel2`
--

DROP TABLE IF EXISTS `causes_nonprofits_rel2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `causes_nonprofits_rel2` (
  `causes_nonprofits_rel2_id` int(11) NOT NULL AUTO_INCREMENT,
  `nonprofit_id` int(11) NOT NULL,
  `cause_name` varchar(45) NOT NULL,
  `weight` int(11) DEFAULT NULL,
  PRIMARY KEY (`causes_nonprofits_rel2_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4379 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `companies` (
  `companies_id` int(11) NOT NULL AUTO_INCREMENT,
  `ticker` varchar(45) NOT NULL,
  `name` varchar(150) NOT NULL,
  `exchange` varchar(45) NOT NULL,
  `website` varchar(150) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `sector` varchar(100) NOT NULL,
  `summary` varchar(1000) NOT NULL,
  PRIMARY KEY (`companies_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65536 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `company_cause_match`
--

DROP TABLE IF EXISTS `company_cause_match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_cause_match` (
  `match_id` int(11) NOT NULL,
  `company_db_id` int(11) NOT NULL,
  `cause_db_id` int(11) NOT NULL,
  PRIMARY KEY (`match_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `news_articles`
--

DROP TABLE IF EXISTS `news_articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_articles` (
  `news_articles_id` int(11) NOT NULL AUTO_INCREMENT,
  `nonprofits_id` int(11) NOT NULL,
  `insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `url` varchar(500) NOT NULL,
  `headline` varchar(500) DEFAULT NULL,
  `text` text,
  PRIMARY KEY (`news_articles_id`),
  KEY `insert_time` (`insert_time`),
  KEY `FK_nonprofits_id_idx` (`nonprofits_id`),
  CONSTRAINT `FK_nonprofits_id` FOREIGN KEY (`nonprofits_id`) REFERENCES `nonprofits` (`nonprofits_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3967 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `news_articles_companies_rel`
--

DROP TABLE IF EXISTS `news_articles_companies_rel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_articles_companies_rel` (
  `news_articles_companies_rel_id` int(11) NOT NULL AUTO_INCREMENT,
  `news_articles_id` int(11) NOT NULL,
  `companies_id` int(11) NOT NULL,
  PRIMARY KEY (`news_articles_companies_rel_id`),
  KEY `FK_news_articles_id_idx` (`news_articles_id`),
  KEY `FK_companies_id_idx` (`companies_id`)
) ENGINE=InnoDB AUTO_INCREMENT=737 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofit_twitter_attributes`
--

DROP TABLE IF EXISTS `nonprofit_twitter_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofit_twitter_attributes` (
  `nonprofit_twitter_attributes_id` int(11) NOT NULL AUTO_INCREMENT,
  `nonprofit_id` int(11) DEFAULT NULL,
  `id` varchar(45) NOT NULL,
  `label` varchar(45) NOT NULL,
  `degree` int(11) DEFAULT NULL,
  `weighted_degree` int(11) DEFAULT NULL,
  `eccentricity` int(11) DEFAULT NULL,
  `closeness_centrality` decimal(25,20) DEFAULT NULL,
  `betweenness_centrality` decimal(25,20) DEFAULT NULL,
  `modularity_class` int(11) DEFAULT NULL,
  `authority` decimal(25,20) DEFAULT NULL,
  `hub` decimal(25,20) DEFAULT NULL,
  `clustering_coefficient` decimal(25,20) DEFAULT NULL,
  `number_of_triangles` int(11) DEFAULT NULL,
  `weighted_clustering_coefficient` decimal(25,20) DEFAULT NULL,
  `strength` int(11) DEFAULT NULL,
  `eigenvector_centrality` decimal(25,20) DEFAULT NULL,
  `number_of_followers` int(11) DEFAULT NULL,
  PRIMARY KEY (`nonprofit_twitter_attributes_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1178 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofit_twitter_edges`
--

DROP TABLE IF EXISTS `nonprofit_twitter_edges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofit_twitter_edges` (
  `nonprofit_twitter_edges_id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(45) NOT NULL,
  `target` varchar(45) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `edge_id` int(11) DEFAULT NULL,
  `label` varchar(45) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `community` int(11) DEFAULT NULL,
  `neighborhood_overlap` decimal(25,20) DEFAULT NULL,
  `embeddedness` int(11) DEFAULT NULL,
  PRIMARY KEY (`nonprofit_twitter_edges_id`)
) ENGINE=InnoDB AUTO_INCREMENT=412285 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofit_websites`
--

DROP TABLE IF EXISTS `nonprofit_websites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofit_websites` (
  `nonprofit_websites_id` int(10) NOT NULL AUTO_INCREMENT,
  `nonprofit_id` int(11) NOT NULL,
  `website` varchar(200) NOT NULL,
  PRIMARY KEY (`nonprofit_websites_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6126 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits`
--

DROP TABLE IF EXISTS `nonprofits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits` (
  `nonprofits_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `ein` varchar(45) DEFAULT NULL,
  `ntee_code` varchar(200) DEFAULT NULL,
  `mission_statement` varchar(6000) DEFAULT NULL,
  `description` varchar(6000) DEFAULT NULL,
  `twitter_id` varchar(100) DEFAULT NULL,
  `twitter_name` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `ZIP` varchar(45) DEFAULT NULL,
  `revenue` int(15) DEFAULT NULL,
  `year` year(4) DEFAULT NULL,
  PRIMARY KEY (`nonprofits_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23187 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_communities_by_description`
--

DROP TABLE IF EXISTS `nonprofits_communities_by_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_communities_by_description` (
  `nonprofits_id` int(11) NOT NULL,
  `causes_id` int(11) NOT NULL,
  `community` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_communities_by_description_words`
--

DROP TABLE IF EXISTS `nonprofits_communities_by_description_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_communities_by_description_words` (
  `causes_id` int(11) NOT NULL,
  `community` int(11) NOT NULL,
  `word1` varchar(45) DEFAULT NULL,
  `count1` int(11) DEFAULT NULL,
  `word2` varchar(45) DEFAULT NULL,
  `count2` int(11) DEFAULT NULL,
  `word3` varchar(45) DEFAULT NULL,
  `count3` int(11) DEFAULT NULL,
  `word4` varchar(45) DEFAULT NULL,
  `count4` int(11) DEFAULT NULL,
  `word5` varchar(45) DEFAULT NULL,
  `count5` int(11) DEFAULT NULL,
  `word6` varchar(45) DEFAULT NULL,
  `count6` int(11) DEFAULT NULL,
  `word7` varchar(45) DEFAULT NULL,
  `count7` int(11) DEFAULT NULL,
  `word8` varchar(45) DEFAULT NULL,
  `count8` int(11) DEFAULT NULL,
  `word9` varchar(45) DEFAULT NULL,
  `count9` int(11) DEFAULT NULL,
  `word10` varchar(45) DEFAULT NULL,
  `count10` int(11) DEFAULT NULL,
  `word11` varchar(45) DEFAULT NULL,
  `count11` int(11) DEFAULT NULL,
  `word12` varchar(45) DEFAULT NULL,
  `count12` int(11) DEFAULT NULL,
  `word13` varchar(45) DEFAULT NULL,
  `count13` int(11) DEFAULT NULL,
  `word14` varchar(45) DEFAULT NULL,
  `count14` int(11) DEFAULT NULL,
  `word15` varchar(45) DEFAULT NULL,
  `count15` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_communities_by_homepage`
--

DROP TABLE IF EXISTS `nonprofits_communities_by_homepage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_communities_by_homepage` (
  `nonprofits_id` int(11) NOT NULL,
  `causes_id` int(11) NOT NULL,
  `community` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_communities_by_homepage_words`
--

DROP TABLE IF EXISTS `nonprofits_communities_by_homepage_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_communities_by_homepage_words` (
  `causes_id` int(11) NOT NULL,
  `community` int(11) NOT NULL,
  `word1` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count1` int(11) DEFAULT NULL,
  `word2` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count2` int(11) DEFAULT NULL,
  `word3` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count3` int(11) DEFAULT NULL,
  `word4` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count4` int(11) DEFAULT NULL,
  `word5` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count5` int(11) DEFAULT NULL,
  `word6` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count6` int(11) DEFAULT NULL,
  `word7` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count7` int(11) DEFAULT NULL,
  `word8` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count8` int(11) DEFAULT NULL,
  `word9` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count9` int(11) DEFAULT NULL,
  `word10` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count10` int(11) DEFAULT NULL,
  `word11` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count11` int(11) DEFAULT NULL,
  `word12` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count12` int(11) DEFAULT NULL,
  `word13` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count13` int(11) DEFAULT NULL,
  `word14` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count14` int(11) DEFAULT NULL,
  `word15` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count15` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_communities_by_tweets`
--

DROP TABLE IF EXISTS `nonprofits_communities_by_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_communities_by_tweets` (
  `nonprofits_id` int(11) DEFAULT NULL,
  `causes_id` int(11) DEFAULT NULL,
  `community` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_communities_by_tweets_words`
--

DROP TABLE IF EXISTS `nonprofits_communities_by_tweets_words`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_communities_by_tweets_words` (
  `causes_id` int(11) NOT NULL,
  `community` int(11) NOT NULL,
  `word1` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count1` int(11) DEFAULT NULL,
  `word2` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count2` int(11) DEFAULT NULL,
  `word3` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count3` int(11) DEFAULT NULL,
  `word4` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count4` int(11) DEFAULT NULL,
  `word5` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count5` int(11) DEFAULT NULL,
  `word6` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count6` int(11) DEFAULT NULL,
  `word7` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count7` int(11) DEFAULT NULL,
  `word8` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count8` int(11) DEFAULT NULL,
  `word9` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count9` int(11) DEFAULT NULL,
  `word10` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count10` int(11) DEFAULT NULL,
  `word11` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count11` int(11) DEFAULT NULL,
  `word12` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count12` int(11) DEFAULT NULL,
  `word13` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count13` int(11) DEFAULT NULL,
  `word14` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count14` int(11) DEFAULT NULL,
  `word15` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count15` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_followers`
--

DROP TABLE IF EXISTS `nonprofits_followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_followers` (
  `nonprofit_handle` varchar(45) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_similarity_by_description`
--

DROP TABLE IF EXISTS `nonprofits_similarity_by_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_similarity_by_description` (
  `nonprofits_similarity_by_description_id` int(11) NOT NULL AUTO_INCREMENT,
  `charity1_id` int(11) NOT NULL,
  `charity2_id` int(11) NOT NULL,
  `similarity` decimal(25,20) DEFAULT NULL,
  PRIMARY KEY (`nonprofits_similarity_by_description_id`),
  KEY `charity1_id` (`charity1_id`),
  KEY `charity2_id` (`charity2_id`),
  KEY `similarity` (`similarity`)
) ENGINE=InnoDB AUTO_INCREMENT=1875420 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_similarity_by_description2`
--

DROP TABLE IF EXISTS `nonprofits_similarity_by_description2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_similarity_by_description2` (
  `nonprofits_similarity_by_description_id` int(11) NOT NULL AUTO_INCREMENT,
  `charity1_id` int(11) NOT NULL,
  `charity2_id` int(11) NOT NULL,
  `similarity` decimal(25,20) DEFAULT NULL,
  PRIMARY KEY (`nonprofits_similarity_by_description_id`),
  KEY `charity1_id` (`charity1_id`),
  KEY `charity2_id` (`charity2_id`),
  KEY `similarity` (`similarity`)
) ENGINE=InnoDB AUTO_INCREMENT=9307860 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_similarity_by_homepage`
--

DROP TABLE IF EXISTS `nonprofits_similarity_by_homepage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_similarity_by_homepage` (
  `nonprofits_similarity_by_homepage` int(11) NOT NULL AUTO_INCREMENT,
  `charity1_id` int(11) NOT NULL,
  `charity2_id` int(11) NOT NULL,
  `similarity` decimal(25,20) NOT NULL,
  PRIMARY KEY (`nonprofits_similarity_by_homepage`),
  KEY `charity1_id` (`charity1_id`),
  KEY `charity2_id` (`charity2_id`),
  KEY `similarity` (`similarity`)
) ENGINE=InnoDB AUTO_INCREMENT=1458298 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_similarity_by_tweets`
--

DROP TABLE IF EXISTS `nonprofits_similarity_by_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_similarity_by_tweets` (
  `nonprofits_similarity_by_tweets_id` int(11) NOT NULL AUTO_INCREMENT,
  `twitter_name1` varchar(45) NOT NULL,
  `twitter_name2` varchar(45) NOT NULL,
  `similarity` decimal(25,20) NOT NULL,
  PRIMARY KEY (`nonprofits_similarity_by_tweets_id`),
  KEY `name1` (`twitter_name1`),
  KEY `name2` (`twitter_name2`)
) ENGINE=InnoDB AUTO_INCREMENT=1235329 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_similarity_by_tweets2`
--

DROP TABLE IF EXISTS `nonprofits_similarity_by_tweets2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_similarity_by_tweets2` (
  `nonprofits_similarity_by_tweets_id` int(11) NOT NULL AUTO_INCREMENT,
  `twitter_name1` varchar(45) NOT NULL,
  `twitter_name2` varchar(45) NOT NULL,
  `similarity` decimal(25,20) NOT NULL,
  PRIMARY KEY (`nonprofits_similarity_by_tweets_id`),
  KEY `name1` (`twitter_name1`),
  KEY `name2` (`twitter_name2`)
) ENGINE=InnoDB AUTO_INCREMENT=2556679 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_similarity_by_tweets_ids`
--

DROP TABLE IF EXISTS `nonprofits_similarity_by_tweets_ids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_similarity_by_tweets_ids` (
  `twitter_name1` varchar(45) DEFAULT NULL,
  `twitter_name2` varchar(45) DEFAULT NULL,
  `charity1_id` int(11) DEFAULT NULL,
  `charity2_id` int(11) DEFAULT NULL,
  `similarity` decimal(25,20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_top_words_description`
--

DROP TABLE IF EXISTS `nonprofits_top_words_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_top_words_description` (
  `nonprofits_id` int(11) NOT NULL,
  `word1` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count1` int(11) DEFAULT NULL,
  `word2` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count2` int(11) DEFAULT NULL,
  `word3` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count3` int(11) DEFAULT NULL,
  `word4` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count4` int(11) DEFAULT NULL,
  `word5` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count5` int(11) DEFAULT NULL,
  `word6` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count6` int(11) DEFAULT NULL,
  `word7` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count7` int(11) DEFAULT NULL,
  `word8` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count8` int(11) DEFAULT NULL,
  `word9` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count9` int(11) DEFAULT NULL,
  `word10` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count10` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_top_words_homepage`
--

DROP TABLE IF EXISTS `nonprofits_top_words_homepage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_top_words_homepage` (
  `nonprofits_id` int(11) NOT NULL,
  `word1` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count1` int(11) DEFAULT NULL,
  `word2` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count2` int(11) DEFAULT NULL,
  `word3` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count3` int(11) DEFAULT NULL,
  `word4` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count4` int(11) DEFAULT NULL,
  `word5` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count5` int(11) DEFAULT NULL,
  `word6` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count6` int(11) DEFAULT NULL,
  `word7` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count7` int(11) DEFAULT NULL,
  `word8` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count8` int(11) DEFAULT NULL,
  `word9` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count9` int(11) DEFAULT NULL,
  `word10` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count10` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_top_words_tweets`
--

DROP TABLE IF EXISTS `nonprofits_top_words_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_top_words_tweets` (
  `twitter_name` varchar(45) NOT NULL,
  `word1` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count1` int(11) DEFAULT NULL,
  `word2` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count2` int(11) DEFAULT NULL,
  `word3` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count3` int(11) DEFAULT NULL,
  `word4` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count4` int(11) DEFAULT NULL,
  `word5` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count5` int(11) DEFAULT NULL,
  `word6` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count6` int(11) DEFAULT NULL,
  `word7` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count7` int(11) DEFAULT NULL,
  `word8` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count8` int(11) DEFAULT NULL,
  `word9` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count9` int(11) DEFAULT NULL,
  `word10` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `count10` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nonprofits_tweets`
--

DROP TABLE IF EXISTS `nonprofits_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nonprofits_tweets` (
  `nonprofits_tweets_id` int(11) NOT NULL AUTO_INCREMENT,
  `twitter_name` varchar(45) NOT NULL,
  `tweet_id` varchar(45) NOT NULL,
  `date` varchar(45) DEFAULT NULL,
  `text` varchar(200) DEFAULT NULL,
  `language` varchar(45) DEFAULT NULL,
  `retweet_count` int(11) DEFAULT NULL,
  `favorite_count` int(11) DEFAULT NULL,
  `mentions_ids` varchar(500) DEFAULT NULL,
  `mentions_names` varchar(500) DEFAULT NULL,
  `hashtags` varchar(500) DEFAULT NULL,
  `urls` varchar(500) DEFAULT NULL,
  `in_reply_to_screen_name` varchar(45) DEFAULT NULL,
  `in_reply_to_user_id` varchar(45) DEFAULT NULL,
  `in_reply_to_status_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`nonprofits_tweets_id`),
  KEY `name` (`twitter_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1853769 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-08-26 20:16:52
