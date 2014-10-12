USE food;

CREATE TABLE foodType (
    id	    	INT UNSIGNED NOT NULL AUTO_INCREMENT,
    INDEX	(id),
    PRIMARY KEY	(id),

    nickName	CHAR(4),
    INDEX	(nickName),

    fullName	VARCHAR(80)
);

INSERT INTO foodType
    (id, nickName, fullName)
    VALUES
    (101, 'MF', 'Medifast meal'),
    (102, 'H2O', 'Water'),
    (103, 'Sup', 'Supplements'),
    (104, 'Lean', 'Lean protein'),
    (105, 'Grn', 'Green vegetables'),
    (106, 'Ex', 'Exercise'),
    (107, 'Off', 'Off-plan food');

CREATE TABLE foodLog (
    id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
    INDEX	  (id),
    PRIMARY KEY   (id),

    atype	  INT UNSIGNED NOT NULL,
    FOREIGN KEY	  (atype) REFERENCES foodType (id),
    INDEX   	  (atype),

    btype	  VARCHAR(80),
    stamp 	  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    quantity  	  INT UNSIGNED,
    comment	  VARCHAR(240)
);

CREATE TABLE weight (
    id            INT UNSIGNED NOT NULL AUTO_INCREMENT,
    INDEX         (id),
    PRIMARY KEY   (id),

    stamp         TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL;
    weight        FLOAT,
    note          VARCHAR(240)
);
