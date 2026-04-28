-- add phone
CREATE OR REPLACE PROCEDURE add_phone(
    p_first TEXT,
    p_last TEXT,
    p_phone TEXT,
    p_type TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid
    FROM contacts
    WHERE first_name = p_first AND last_name = p_last
    LIMIT 1;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;


-- move to group
CREATE OR REPLACE PROCEDURE move_to_group(
    p_name TEXT,
    p_group TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group;

    UPDATE contacts
    SET group_id = gid
    WHERE first_name = p_name;
END;
$$;


-- search function
CREATE OR REPLACE FUNCTION search_contacts(q TEXT)
RETURNS TABLE (
    id INT,
    first_name TEXT,
    last_name TEXT,
    email TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT id, first_name, last_name, email
    FROM contacts
    WHERE first_name ILIKE '%'||q||'%'
       OR last_name ILIKE '%'||q||'%'
       OR email ILIKE '%'||q||'%';
END;
$$ LANGUAGE plpgsql;