-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema facebook
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema facebook
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `facebook` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `facebook` ;

-- -----------------------------------------------------
-- Table `facebook`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(1000) NOT NULL,
  `avatar` VARCHAR(255) NULL DEFAULT 'user-default.png',
  `background` VARCHAR(255) NULL DEFAULT 'unnamed.jpg',
  `DOB` VARCHAR(50) NOT NULL,
  `place` VARCHAR(255) NOT NULL,
  `school` VARCHAR(255) NOT NULL,
  `company` VARCHAR(255) NOT NULL,
  `last_seen` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `phone` VARCHAR(16) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 38
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `facebook`.`conversations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`conversations` (
  `conversation_id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(40) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`conversation_id`),
  INDEX `fk_conversations_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_conversations_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `facebook`.`chats`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`chats` (
  `chat_id` INT NOT NULL AUTO_INCREMENT,
  `from_id` INT NOT NULL,
  `to_id` INT NOT NULL,
  `message` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sender_id` INT NOT NULL,
  `participants_id` INT NOT NULL,
  `conversation_id` INT NOT NULL,
  PRIMARY KEY (`chat_id`),
  INDEX `fk_chats_conversations1_idx` (`conversation_id` ASC),
  CONSTRAINT `fk_chats_conversations1`
    FOREIGN KEY (`conversation_id`)
    REFERENCES `facebook`.`conversations` (`conversation_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 31
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `facebook`.`comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`comment` (
  `chat_id` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`chat_id`),
  INDEX `fk_comment_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_comment_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 231
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `facebook`.`blogs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`blogs` (
  `blog_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `body` TEXT NOT NULL,
  `status` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`blog_id`),
  INDEX `fk_blogs_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_blogs_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `facebook`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`likes` (
  `like_id` INT NOT NULL,
  `chat_id` INT NOT NULL,
  `blogs_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `time` TIMESTAMP NOT NULL,
  PRIMARY KEY (`like_id`),
  INDEX `fk_likes_comment1_idx` (`chat_id` ASC),
  INDEX `fk_likes_blogs1_idx` (`blogs_id` ASC),
  INDEX `fk_likes_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_likes_comment1`
    FOREIGN KEY (`chat_id`)
    REFERENCES `facebook`.`comment` (`chat_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_blogs1`
    FOREIGN KEY (`blogs_id`)
    REFERENCES `facebook`.`blogs` (`blog_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `facebook`.`follows`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`follows` (
  `created_at` DATETIME NOT NULL,
  `following_user_id` INT NOT NULL,
  `followed_user_id` INT NOT NULL,
  `time` TIMESTAMP NULL,
  INDEX `fk_follows_users1_idx` (`following_user_id` ASC),
  INDEX `fk_follows_users2_idx` (`followed_user_id` ASC),
  CONSTRAINT `fk_follows_users1`
    FOREIGN KEY (`following_user_id`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_follows_users2`
    FOREIGN KEY (`followed_user_id`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `facebook`.`friend`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `facebook`.`friend` (
  `friend_id_1` INT NOT NULL,
  `friend_id_2` INT NOT NULL,
  `friend_id` INT NOT NULL,
  `time` TIMESTAMP NOT NULL,
  INDEX `fk_friend_users1_idx` (`friend_id_1` ASC),
  INDEX `fk_friend_users2_idx` (`friend_id_2` ASC),
  PRIMARY KEY (`friend_id`),
  CONSTRAINT `fk_friend_users1`
    FOREIGN KEY (`friend_id_1`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_friend_users2`
    FOREIGN KEY (`friend_id_2`)
    REFERENCES `facebook`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
