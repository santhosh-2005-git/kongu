# Farmers Management System

A GUI-based DBMS project using Python (Tkinter) and MySQL for managing farmer records.

## Structure
- `frontend/`: GUI using Tkinter.
- `backend/`: Database config and CRUD operations.
- `assets/`: Images for GUI backgrounds.

## Requirements
- Python 3
- MySQL
- `mysql-connector-python`
- `Pillow` (for image handling)

## How to Run
1. Start your MySQL server.
2. Create the database and table.
3. Run `frontend/main.py`.

## Database Table
```sql
CREATE DATABASE farmer_db;
USE farmer_db;

CREATE TABLE farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    crop_type VARCHAR(50),
    location VARCHAR(100),
    phone VARCHAR(15),
    farm_size VARCHAR(20),
    soil_type VARCHAR(50),
    irrigation VARCHAR(50)
);
