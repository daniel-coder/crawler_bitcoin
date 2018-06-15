CREATE TABLE `test.bit_news` (
  `url` varchar(256) CHARACTER SET ascii NOT NULL,
  `title` varchar(256) NOT NULL DEFAULT '' COMMENT '标题',
  `time` datetime DEFAULT NULL COMMENT '时间',
  `read_count` INT NOT NULL DEFAULT 0  COMMENT '浏览数',
  `content` mediumtext NOT NULL COMMENT '内容',
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS test.bit_messages;
CREATE TABLE test.bit_messages (
  `url` varchar(255) NOT NULL COMMENT '链接地址',
  `title` varchar(256) NOT NULL DEFAULT '' COMMENT '标题',
  `time` datetime DEFAULT NULL COMMENT '时间',
  `up` INT NOT NULL DEFAULT 0  COMMENT '看多',
  `down` INT NOT NULL DEFAULT 0  COMMENT '看空',
  `content` mediumtext NOT NULL COMMENT '内容',
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;