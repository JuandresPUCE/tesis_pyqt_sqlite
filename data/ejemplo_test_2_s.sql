BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "condiciones_iniciales" (
	"id"	INTEGER NOT NULL,
	"temperatura"	FLOAT,
	"tiempo"	FLOAT,
	"presion_total"	FLOAT,
	"presion_parcial"	FLOAT,
	"fraccion_molar"	FLOAT,
	"especie_quimica"	VARCHAR,
	"tipo_especie"	VARCHAR,
	"detalle"	VARCHAR,
	"nombre_data"	VARCHAR,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "datos_ingresados_cineticos" (
	"id"	INTEGER NOT NULL,
	"tiempo"	FLOAT NOT NULL,
	"concentracion"	FLOAT,
	"otra_propiedad"	FLOAT,
	"conversion_reactivo_limitante"	FLOAT,
	"tipo_especie"	VARCHAR,
	"id_condiciones_iniciales"	INTEGER,
	"nombre_data"	VARCHAR,
	"nombre_reaccion"	VARCHAR,
	"especie_quimica"	VARCHAR,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "registro_data_experimental" (
	"id"	INTEGER NOT NULL,
	"nombre_data"	VARCHAR,
	"fecha"	VARCHAR,
	"detalle"	VARCHAR,
	PRIMARY KEY("id"),
	UNIQUE("nombre_data")
);
CREATE TABLE IF NOT EXISTS "reaccion_quimica" (
	"id"	INTEGER NOT NULL,
	"especie_quimica"	VARCHAR,
	"formula"	VARCHAR,
	"coeficiente_estequiometrico"	FLOAT,
	"detalle"	VARCHAR,
	"tipo_especie"	VARCHAR,
	"nombre_reaccion"	VARCHAR,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "registro_unidades" (
	"id"	INTEGER NOT NULL,
	"presion"	VARCHAR,
	"temperatura"	VARCHAR,
	"tiempo"	VARCHAR,
	"concentracion"	VARCHAR,
	"energia"	VARCHAR,
	"r"	FLOAT,
	"nombre_data"	VARCHAR,
	PRIMARY KEY("id"),
	UNIQUE("nombre_data")
);
CREATE TABLE IF NOT EXISTS "datos_salida" (
	"id"	INTEGER NOT NULL,
	"nombre_data_salida"	VARCHAR,
	"fecha"	VARCHAR,
	"id_nombre_data"	INTEGER,
	"id_condiciones_iniciales"	INTEGER,
	"id_registro_unidades"	INTEGER,
	"r_utilizada"	FLOAT,
	"nombre_data"	VARCHAR,
	"nombre_reaccion"	VARCHAR,
	"delta_n_reaccion"	FLOAT,
	"epsilon_reactivo_limitante"	FLOAT,
	"tipo_especie"	VARCHAR,
	"especie_quimica"	VARCHAR,
	"constante_cinetica"	FLOAT,
	"orden_reaccion"	FLOAT,
	"modelo_cinetico"	VARCHAR,
	"tipo_calculo"	VARCHAR,
	"energia_activacion"	FLOAT,
	"detalles"	VARCHAR,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "datos_salida_proceso_arrhenius" (
	"id"	INTEGER NOT NULL,
	"nombre_caso"	VARCHAR,
	"id_nombre_data_salida"	INTEGER,
	"id_nombre_data"	INTEGER,
	"fecha"	VARCHAR,
	"temperatura"	FLOAT,
	"reciproco_temperatura_absoluta"	FLOAT,
	"constante_cinetica"	FLOAT,
	"logaritmo_constante_cinetica"	FLOAT,
	"energia_activacion_r"	FLOAT,
	"r_utilizada"	FLOAT,
	"energia_activacion"	FLOAT,
	"constante_cinetica_0"	FLOAT,
	"logaritmo_constante_cinetica_0"	FLOAT,
	"detalles"	VARCHAR,
	PRIMARY KEY("id")
);
COMMIT;
