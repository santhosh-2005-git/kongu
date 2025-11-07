CREATE TABLE farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    crop_type VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    phone VARCHAR(15),
    farm_size VARCHAR(50),
    soil_type VARCHAR(100),
    irrigation VARCHAR(100)
);
