CREATE TABLE public.registros (
    id SERIAL PRIMARY KEY,
    nombre character varying(100) NOT NULL,
    comuna integer NOT NULL,
    fecha_ingreso timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    carrera character varying(50) NOT NULL,
    idioma character varying(20) NOT NULL
);