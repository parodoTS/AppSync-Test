--función para devolver Pacientes con sus departamentos

--DROP FUNCTION getpajson(integer);
CREATE OR REPLACE FUNCTION getPaJson(FRSid int) 
RETURNS table (j json) AS
$$
BEGIN
RETURN QUERY  select json_agg(t) from (select *, (select json_agg(r) from (select departamento.* from tratamiento INNER JOIN departamento ON departamento.id=tratamiento.departamento_ID where paciente.id=tratamiento.paciente_id)r)as department from paciente where paciente.id=FRSid)t;
END;
$$ LANGUAGE plpgsql;
