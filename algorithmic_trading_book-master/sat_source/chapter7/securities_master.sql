-- Create the 'exchange' table
CREATE TABLE `exchange` (
  `id` int NOT NULL AUTO_INCREMENT,
  `abbrev` varchar(32) NOT NULL,
  `name` varchar(255) NOT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `currency` varchar(64) DEFAULT NULL,
  `timezone_offset` time DEFAULT NULL,
  `created_date` datetime NOT NULL,
  `last_updated_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- Create the 'data_vendor' table
CREATE TABLE `data_vendor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `website_url` varchar(255) DEFAULT NULL,
  `support_email` varchar(255) DEFAULT NULL,
  `created_date` datetime NOT NULL,
  `last_updated_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- Create the 'symbol' table
CREATE TABLE `symbol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exchange_id` int DEFAULT NULL,
  `ticker` varchar(32) NOT NULL,
  `instrument` varchar(64) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `sector` varchar(255) DEFAULT NULL,
  `currency` varchar(32) DEFAULT NULL,
  `created_date` datetime NOT NULL,
  `last_updated_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `index_exchange_id` (`exchange_id`),
  CONSTRAINT `fk_symbol_exchange_id` FOREIGN KEY (`exchange_id`) REFERENCES `exchange` (`id`)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- Create the 'daily_price' table
CREATE TABLE `daily_price` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_vendor_id` int NOT NULL,
  `symbol_id` int NOT NULL,
  `price_date` datetime NOT NULL,
  `created_date` datetime NOT NULL,
  `last_updated_date` datetime NOT NULL,
  `open_price` decimal(19,4) DEFAULT NULL,
  `high_price` decimal(19,4) DEFAULT NULL,
  `low_price` decimal(19,4) DEFAULT NULL,
  `close_price` decimal(19,4) DEFAULT NULL,
  `adj_close_price` decimal(19,4) DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_data_vendor_id` (`data_vendor_id`),
  KEY `index_symbol_id` (`symbol_id`),
  CONSTRAINT `fk_daily_price_data_vendor_id` FOREIGN KEY (`data_vendor_id`) REFERENCES `data_vendor` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_daily_price_symbol_id` FOREIGN KEY (`symbol_id`) REFERENCES `symbol` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
