SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema anjunabot-dev
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema anjunabot-dev
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `anjunabot-dev` DEFAULT CHARACTER SET latin1 ;
USE `anjunabot-dev` ;

-- -----------------------------------------------------
-- Table `anjunabot-dev`.`message_stage`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`message_stage` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`message_stage` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `path` VARCHAR(512) NOT NULL,
  `path_type` VARCHAR(48) NULL,
  `first_name` VARCHAR(64) NOT NULL,
  `last_name` VARCHAR(64) NULL,
  `text` VARCHAR(1024) NOT NULL,
  `chat_id` INT NOT NULL,
  `chat_title` VARCHAR(128) NOT NULL,
  `platform` VARCHAR(48) NOT NULL,
  `date_added` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 36
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`person`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`person` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`person` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(64) NULL,
  `last_name` VARCHAR(64) NULL,
  `state` VARCHAR(64) NULL,
  `date_added` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`chat`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`chat` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`chat` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cid` INT NULL,
  `title` VARCHAR(128) NULL,
  `date_added` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`path`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`path` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`path` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(48) NULL,
  `uri` VARCHAR(512) NULL,
  `platform` VARCHAR(45) NULL,
  `date_added` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`post` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`post` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `chat_id` INT NULL,
  `path_id` INT NULL,
  `person_id` INT NULL,
  `text` VARCHAR(1024) NOT NULL,
  `date_added` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_post_chat1_idx` (`chat_id` ASC),
  INDEX `fk_post_person1_idx` (`person_id` ASC),
  INDEX `fk_post_path1_idx` (`path_id` ASC),
  CONSTRAINT `fk_post_chat1`
    FOREIGN KEY (`chat_id`)
    REFERENCES `anjunabot-dev`.`chat` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_person1`
    FOREIGN KEY (`person_id`)
    REFERENCES `anjunabot-dev`.`person` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_path1`
    FOREIGN KEY (`path_id`)
    REFERENCES `anjunabot-dev`.`path` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`track`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`track` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`track` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `path_id` INT NULL,
  `title` VARCHAR(256) NULL,
  `date_added` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_track_path1_idx` (`path_id` ASC),
  CONSTRAINT `fk_track_path1`
    FOREIGN KEY (`path_id`)
    REFERENCES `anjunabot-dev`.`path` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`album`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`album` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`album` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(256) NULL,
  `type` VARCHAR(64) NULL,
  `num_tracks` INT NULL,
  `artist_id` INT NULL,
  `track_id` INT NULL,
  `path_id` INT NULL,
  `date_added` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_album_path1_idx` (`path_id` ASC),
  CONSTRAINT `fk_album_path1`
    FOREIGN KEY (`path_id`)
    REFERENCES `anjunabot-dev`.`path` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`artist` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`artist` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `path_id` INT NULL,
  `name` VARCHAR(256) NULL,
  `date_added` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_artist_path1_idx` (`path_id` ASC),
  CONSTRAINT `fk_artist_path1`
    FOREIGN KEY (`path_id`)
    REFERENCES `anjunabot-dev`.`path` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`track_artists`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`track_artists` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`track_artists` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `track_id` INT NULL,
  `artist_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_track_artists_track1_idx` (`track_id` ASC),
  INDEX `fk_track_artists_artist1_idx` (`artist_id` ASC),
  CONSTRAINT `fk_track_artists_track1`
    FOREIGN KEY (`track_id`)
    REFERENCES `anjunabot-dev`.`track` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_track_artists_artist1`
    FOREIGN KEY (`artist_id`)
    REFERENCES `anjunabot-dev`.`artist` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`album_tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`album_tracks` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`album_tracks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `album_id` INT NULL,
  `track_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_album_tracks_track1_idx` (`track_id` ASC),
  INDEX `fk_album_tracks_album1_idx` (`album_id` ASC),
  CONSTRAINT `fk_album_tracks_track1`
    FOREIGN KEY (`track_id`)
    REFERENCES `anjunabot-dev`.`track` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_album_tracks_album1`
    FOREIGN KEY (`album_id`)
    REFERENCES `anjunabot-dev`.`album` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`playlist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`playlist` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`playlist` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `path_id` INT NULL,
  `title` VARCHAR(256) NULL,
  `date_added` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_playlist_path1_idx` (`path_id` ASC),
  CONSTRAINT `fk_playlist_path1`
    FOREIGN KEY (`path_id`)
    REFERENCES `anjunabot-dev`.`path` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anjunabot-dev`.`playlist_tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `anjunabot-dev`.`playlist_tracks` ;

CREATE TABLE IF NOT EXISTS `anjunabot-dev`.`playlist_tracks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `playlist_id` INT NULL,
  `track_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_playlist_tracks_playlist1_idx` (`playlist_id` ASC),
  INDEX `fk_playlist_tracks_track1_idx` (`track_id` ASC),
  CONSTRAINT `fk_playlist_tracks_playlist1`
    FOREIGN KEY (`playlist_id`)
    REFERENCES `anjunabot-dev`.`playlist` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_playlist_tracks_track1`
    FOREIGN KEY (`track_id`)
    REFERENCES `anjunabot-dev`.`track` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
