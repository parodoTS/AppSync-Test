CREATE TABLE director (id serial, nombre varchar(100), apellido varchar(100), PRIMARY KEY(ID));
		insert into director (nombre, apellido) values ('albert', 'einstein');
		insert into director (nombre, apellido) values ('isaac', 'newton');
		insert into director (nombre, apellido) values ('marie', 'curie');
	

create table hospital (id serial, ubicacion varchar(100), nombre varchar(100), director_id int, PRIMARY KEY(ID),CONSTRAINT fk_director FOREIGN KEY(director_ID) REFERENCES director(ID));
		insert into hospital (ubicacion, nombre, director_id) values ('Granada', 'Virgen de las Nieves', 2);
		insert into hospital (ubicacion, nombre, director_id) values ('Jaen', 'San Agustin', 3);
		insert into hospital (ubicacion, nombre, director_id) values ('Barcelona', 'Hospital Clinic', 1);
	


create table doctor (id serial, nombre varchar(100), apellido varchar(100), hospital_id int, PRIMARY KEY(ID),CONSTRAINT fk_hospital FOREIGN KEY(hospital_ID) REFERENCES hospital(ID));
		insert into doctor (nombre, apellido, hospital_id) values ('Juan', 'Rodrigo', 3);
		insert into doctor (nombre, apellido, hospital_id) values ('Manuel', 'Carrasco', 2);
		insert into doctor (nombre, apellido, hospital_id) values ('David', 'Muñoz', 1);
		

create table departamento (id serial, nombre varchar(100), PRIMARY KEY(ID));
		insert into departamento (nombre) values ('UCI');
		insert into departamento (nombre) values ('Cirugía');
		insert into departamento (nombre) values ('Pediatría');
		

create table consulta (id serial NOT NULL, doctor_ID int NOT NULL, departamento_ID int NOT NULL, PRIMARY KEY(ID),CONSTRAINT fk_departamento FOREIGN KEY(departamento_ID) REFERENCES departamento(ID) ON DELETE CASCADE, CONSTRAINT fk_doctor FOREIGN KEY(doctor_ID) REFERENCES doctor(ID) ON DELETE CASCADE);
		insert into consulta (doctor_ID, departamento_ID) values (1,1);
		insert into consulta (doctor_ID, departamento_ID) values (2,2);
		insert into consulta (doctor_ID, departamento_ID) values (3,3);
		


create table paciente (id serial, nombre varchar(100) NOT NULL, apellido varchar(100) NOT NULL, direccion varchar(100) NOT NULL, PRIMARY KEY(ID));
		insert into paciente (nombre, apellido, direccion) values ('Fernando', 'Rey', 'C/ Pintor');
		insert into paciente (nombre, apellido, direccion) values ('Esther', 'Nuñez', 'Avda/ Antonio');
		insert into paciente (nombre, apellido, direccion) values ('Esteban', 'Ruiz', 'C/ Real');
		


create table tratamiento (id serial NOT NULL, paciente_ID int NOT NULL, departamento_ID int NOT NULL, PRIMARY KEY(ID),CONSTRAINT fk_departamento FOREIGN KEY(departamento_ID) REFERENCES departamento(ID) ON DELETE CASCADE, CONSTRAINT fk_paciente FOREIGN KEY(paciente_ID) REFERENCES paciente(ID) ON DELETE CASCADE);
		insert into tratamiento (paciente_ID, departamento_ID) values (2, 1);
		insert into tratamiento (paciente_ID, departamento_ID) values (1, 3);
		insert into tratamiento (paciente_ID, departamento_ID) values (3,2 );
			
