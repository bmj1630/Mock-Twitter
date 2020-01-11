-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema pyexam
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pyexam
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pyexam` DEFAULT CHARACTER SET utf8 ;
USE `pyexam` ;

-- -----------------------------------------------------
-- Table `pyexam`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pyexam`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `pyexam`.`thoughts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pyexam`.`thoughts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `author` INT(11) NOT NULL,
  `message` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_thoughts_users_idx` (`author` ASC) VISIBLE,
  CONSTRAINT `fk_thoughts_users`
    FOREIGN KEY (`author`)
    REFERENCES `pyexam`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `pyexam`.`users_has_thoughts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pyexam`.`users_has_thoughts` (
  `user_id` INT(11) NOT NULL,
  `thought_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `thought_id`),
  INDEX `fk_users_has_thoughts_thoughts1_idx` (`thought_id` ASC) VISIBLE,
  INDEX `fk_users_has_thoughts_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_thoughts_thoughts1`
    FOREIGN KEY (`thought_id`)
    REFERENCES `pyexam`.`thoughts` (`id`),
  CONSTRAINT `fk_users_has_thoughts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `pyexam`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
