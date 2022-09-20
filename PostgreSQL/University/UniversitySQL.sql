CREATE TABLE decano (id serial, nombre varchar(100), apellido varchar(100), PRIMARY KEY(ID));
		insert into decano (nombre, apellido) values ('albert', 'einstein');
		insert into decano (nombre, apellido) values ('isaac', 'newton');
		insert into decano (nombre, apellido) values ('marie', 'curie');
	

create table facultad (id serial, ubicacion varchar(100), nombre varchar(100), decano_id int, PRIMARY KEY(ID),CONSTRAINT fk_decano FOREIGN KEY(decano_ID) REFERENCES decano(ID));
		insert into facultad (ubicacion, nombre, decano_id) values ('Granada', 'Ciencia', 2);
		insert into facultad (ubicacion, nombre, decano_id) values ('Jaen', 'UJA', 3);
		insert into facultad (ubicacion, nombre, decano_id) values ('Barcelona', 'Universidad Autonoma', 1);
	


create table profesor (id serial, nombre varchar(100), apellido varchar(100), facultad_id int, PRIMARY KEY(ID),CONSTRAINT fk_facultad FOREIGN KEY(facultad_ID) REFERENCES facultad(ID));
		insert into profesor (nombre, apellido, facultad_id) values ('Alvaro', 'Torno', 3);
		insert into profesor (nombre, apellido, facultad_id) values ('Maria', 'Raez', 2);
		insert into profesor (nombre, apellido, facultad_id) values ('Sofia', 'Alamo', 1);
		

create table asignatura (id serial, nombre varchar(100), creditos int NOT NULL, PRIMARY KEY(ID));
		insert into asignatura (nombre, creditos) values ('Matematicas', 312);
		insert into asignatura (nombre, creditos) values ('Informatica', 412);
		insert into asignatura (nombre, creditos) values ('Despliegue Web', 1);
		

create table curso (id serial NOT NULL, PROFESOR_ID int NOT NULL, ASIGNATURA_ID int NOT NULL, PRIMARY KEY(ID),CONSTRAINT fk_ASIGNATURA FOREIGN KEY(ASIGNATURA_ID) REFERENCES ASIGNATURA(ID), CONSTRAINT fk_PROFESOR FOREIGN KEY(PROFESOR_ID) REFERENCES PROFESOR(ID));
		insert into curso (PROFESOR_ID, ASIGNATURA_ID) values (1,1);
		insert into curso (PROFESOR_ID, ASIGNATURA_ID) values (2,2);
		insert into curso (PROFESOR_ID, ASIGNATURA_ID) values (3,3);
		


create table estudiante (id serial, nombre varchar(100) NOT NULL, apellido varchar(100) NOT NULL, direccion varchar(100) NOT NULL, PRIMARY KEY(ID));
		insert into estudiante (nombre, apellido, direccion) values ('Francisco', 'Navega', 'C/ Malaga');
		insert into estudiante (nombre, apellido, direccion) values ('Jose Luis', 'Fernandez', 'C/ Villa');
		insert into estudiante (nombre, apellido, direccion) values ('Maria Jose', 'Rubio', 'Avda/ Glorieta');
		


create table matricula (id serial NOT NULL, ESTUDIANTE_ID int NOT NULL, ASIGNATURA_ID int NOT NULL, PRIMARY KEY(ID),CONSTRAINT fk_ASIGNATURA FOREIGN KEY(ASIGNATURA_ID) REFERENCES ASIGNATURA(ID), CONSTRAINT fk_ESTUDIANTE FOREIGN KEY(ESTUDIANTE_ID) REFERENCES ESTUDIANTE(ID));
		insert into matricula (ESTUDIANTE_ID, ASIGNATURA_ID) values (2, 1);
		insert into matricula (ESTUDIANTE_ID, ASIGNATURA_ID) values (1, 3);
		insert into matricula (ESTUDIANTE_ID, ASIGNATURA_ID) values (3,2 );
			
