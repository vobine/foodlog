USE food;

CREATE TABLE foodtype (
    id	    	INT UNSIGNED NOT NULL AUTO_INCREMENT,
    INDEX	(id),
    PRIMARY KEY	(id),

    nickName	CHAR(4),
    INDEX	(nickName),

    fullName	VARCHAR(80)
);

CREATE TABLE foodlog (
    id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
    INDEX	  (id),
    PRIMARY KEY   (id),

    atype	  INT UNSIGNED NOT NULL,
    FOREIGN KEY	  (atype) REFERENCES foodtype (id),
    INDEX   	  (atype),

    btype	  VARCHAR(80),
    stamp 	  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    quantity  	  INT UNSIGNED,
    comment	  VARCHAR(240)
);
