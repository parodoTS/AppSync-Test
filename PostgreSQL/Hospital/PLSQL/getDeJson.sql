--get departamentos con sus doctores

--DROP FUNCTION getDeJson(integer);
CREATE OR REPLACE FUNCTION getDeJson(FRSid int) 
RETURNS table (j json) AS
$$
BEGIN
RETURN QUERY  select json_agg(t) from (select *, (select json_agg(r) from (select doctor.* from consulta INNER JOIN doctor ON doctor.id=consulta.doctor_ID where departamento.id=consulta.departamento_id)r)as department from departamento where departamento.id=FRSid)t;
END;
$$ LANGUAGE plpgsql;

select getDeJson(1)
