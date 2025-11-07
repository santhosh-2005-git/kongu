from backend.db_config import connect_to_db

def save_farmer(vals):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO farmers
          (name, crop_type, location, phone, farm_size, soil_type, irrigation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, vals)
    conn.commit()
    conn.close()

def update_farmer_db(vals, fid):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE farmers SET
          name=%s, crop_type=%s, location=%s, phone=%s,
          farm_size=%s, soil_type=%s, irrigation=%s
        WHERE id=%s
    """, (*vals, fid))
    conn.commit()
    conn.close()

def delete_farmer_db(fid):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM farmers WHERE id=%s", (fid,))
    conn.commit()
    conn.close()

def search_farmer_by_id(fid):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmers WHERE id=%s", (fid,))
    rec = cur.fetchone()
    conn.close()
    return rec

def search_farmer_by_name(name):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmers WHERE name LIKE %s", ('%' + name + '%',))
    recs = cur.fetchall()
    conn.close()
    return recs
