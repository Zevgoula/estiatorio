import sqlite3

conn = sqlite3.connect("SmartRestaurant.db")

cursor = conn.cursor()

commands = [
    """
CREATE TABLE "PELATIS"(
    "id_pelati" INTEGER PRIMARY KEY AUTOINCREMENT,
    "onoma" varchar(20) NOT NULL,
    "eponimo" varchar(20) NOT NULL,
    "tilefono" varchar(13) NOT NULL,
    "email" varchar(20),
    "username" varchar(30),
    "password" varchar(20)
);
""",
    """
CREATE TABLE "TRAPEZI"(
    "id_trapeziou" varchar(10) NOT NULL,
    "thesi" varchar(20),
    "aritmos_theseon" INTEGER NOT NULL CHECK("aritmos_theseon">0),
    
    PRIMARY KEY("id_trapeziou")
);
"""
    ,
    """
CREATE TABLE "KRATISI"(
    "id_kratisis"  INTEGER PRIMARY KEY AUTOINCREMENT,
    "imera_ora" datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    "arithmos_atomon" INTEGER,
    "id_trapeziou" varchar(10) NOT NULL,
    
    FOREIGN KEY("id_trapeziou") REFERENCES "TRAPEZI"("id_trapeziou")
);
""",

    """
CREATE TABLE "KRITIKI"(
    "id" INTEGER NOT NULL UNIQUE ,
    "bathmologia" varchar(8) CHECK("bathmologia">0),
    "perigrafi" varchar(400),
    "imerominia" datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    "id_pelati" INTEGER,
    FOREIGN KEY("id_pelati") REFERENCES "PELATIS"("id_pelati") ,
    PRIMARY KEY("id" AUTOINCREMENT)
);
""",
    """
CREATE TABLE "PARAGGELIA"(
    "id_paraggelias" INTEGER NOT NULL UNIQUE ,
    "imer_ora" datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
    "kostos" REAL CHECK("kostos">=0),
    "id_trapeziou" INTEGER NOT NULL,
    FOREIGN KEY("id_trapeziou") REFERENCES "TRAPEZI"("id_trapeziou"),
    PRIMARY KEY("id_paraggelias" AUTOINCREMENT)
);
""",
    """
CREATE TABLE "MAGEIRAS" (
	"afm_ypallilou"	integer NOT NULL UNIQUE,
	"onoma"	varchar(30) NOT NULL,
	"eponimo"	varchar(50) DEFAULT NULL,
	"misthos"	INTEGER NOT NULL CHECK("misthos>0"),
	"tilefono"	varchar(13) NOT NULL,
	"orario"    varchar (30) NOT NULL,
	PRIMARY KEY("afm_ypallilou")
);
""",
    """
CREATE TABLE "SERVITOROS" (
	"afm_ypallilou"	integer NOT NULL UNIQUE,
	"onoma"	varchar(30) NOT NULL,
	"eponimo"	varchar(50) DEFAULT NULL,
	"misthos"	INTEGER NOT NULL CHECK("misthos>0"),
	"tilefono"	varchar(13) NOT NULL,
	"orario"    varchar (30) NOT NULL,
	PRIMARY KEY("afm_ypallilou")
);
""",
    """

CREATE TABLE "PROMITHEYTIS" (
	"afm"	integer NOT NULL UNIQUE,
	"onoma"	varchar(30) NOT NULL,
	"epitheto"	varchar(50) DEFAULT NULL,
	"tilefono"	integer NOT NULL,
	PRIMARY KEY("afm")
);
""",
    """
CREATE TABLE "YLIKA" (
	"id_ylikoy"	integer NOT NULL UNIQUE ,
	"onoma"	varchar(30) NOT NULL,
	"katigoria"	varchar(50) DEFAULT NULL,
	"diathesimi_posothta"	integer NOT NULL,
	PRIMARY KEY("id_ylikoy" AUTOINCREMENT)
);
""",
    """
CREATE TABLE "FAGITO" (
	"id_fagitoy" INTEGER NOT NULL UNIQUE ,
	"onoma" VARCHAR(30) NOT NULL,
	"kostos" REAL NOT NULL,
	"diathesimothta" INTEGER NOT NULL CHECK ("diathesimothta" >= 0),
	"syntagi" varchar(500) NOT NULL,
    PRIMARY KEY("id_fagitoy" AUTOINCREMENT)
);
""",
    """
CREATE TABLE "POTO" (
	"id_potoy" INTEGER NOT NULL UNIQUE ,
	"onoma" VARCHAR(30) NOT NULL,
	"kostos" REAL NOT NULL CHECK(kostos>0.0),
	"diathesimothta" INTEGER NOT NULL CHECK ("diathesimothta" >= 0),
	PRIMARY KEY("id_potoy" AUTOINCREMENT)
);
""",
    """
CREATE TABLE "PARASKEYAZEI" (
	"afm_ypallilou"	integer NOT NULL,
	"id_fagitoy"	integer NOT NULL,
	FOREIGN KEY("afm_ypallilou") REFERENCES "MAGEIRAS"("afm_ypallilou")
	FOREIGN KEY("id_fagitoy") REFERENCES "FAGITO"("id_fagitoy"),
	PRIMARY KEY("afm_ypallilou","id_fagitoy")
);
""",
    """
CREATE TABLE "APOTELEITAI" (
	"id_fagitoy" integer NOT NULL,
	"id_ylikoy" integer NOT NULL,
	"posotita" integer NOT NULL,
    FOREIGN KEY("id_fagitoy") REFERENCES "FAGITO"("id_fagitoy"),
    FOREIGN KEY("id_ylikoy") REFERENCES "YLIKA"("id_ylikoy"),
	PRIMARY KEY("id_fagitoy","id_ylikoy")
);
""",
    """

CREATE TABLE PERILAMBANEI (
    "id_paraggelias" INTEGER NOT NULL,
    "id_fagitoy" INTEGER,
    "id_potoy" INTEGER,
    "id_perilambanei" INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY ("id_paraggelias") REFERENCES PARAGGELIA("id_paraggelias"),
    FOREIGN KEY ("id_potoy") REFERENCES POTO("id_potoy"),
    FOREIGN KEY ("id_fagitoy") REFERENCES FAGITO("id_fagitoy")
);
""",
    """
CREATE TABLE "ANALAMBANEI" (
	"id_paraggelias" integer NOT NULL,
	"afm_ypallilou"	integer NOT NULL,
    FOREIGN KEY("id_paraggelias") REFERENCES "PARAGGELIA"("id_paraggelias"),
    FOREIGN KEY("afm_ypallilou") REFERENCES "SERVITOROS"("afm_ypallilou"),
    PRIMARY KEY("id_paraggelias","afm_ypallilou")
);
""",
    """
CREATE TABLE "EFODIAZEI" (
	"afm"	integer NOT NULL,
	"id_ylikoy"	integer NOT NULL,
	PRIMARY KEY("id_ylikoy", "afm")
	FOREIGN KEY("afm") REFERENCES "PROMITHEYTIS"("afm") 
	FOREIGN KEY("id_ylikoy") REFERENCES "YLIKA"("id_ylikoy") 
);
""",
    """
CREATE TABLE "PROMITHEVEI" (
	"afm"	integer NOT NULL,
	"id_potoy"	integer NOT NULL,
	"imer_paradosis" datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
	PRIMARY KEY("afm", "id_potoy"),
    FOREIGN KEY("afm") REFERENCES "PROMITHEYTIS"("afm"),
    FOREIGN KEY("id_potoy") REFERENCES "POTO"("id_potoy")
);
""", """
CREATE TABLE "KANEI" (
	"id_pelati"	integer,
	"id_kratisis"	integer NOT NULL,
	FOREIGN KEY("id_pelati") REFERENCES "PELATIS"("id_pelati"),
    FOREIGN KEY("id_kratisis") REFERENCES "KRATISI"("id_kratisis")
);
""",
]

for command in commands:
    conn.execute(command)

conn.commit()
conn.close()
