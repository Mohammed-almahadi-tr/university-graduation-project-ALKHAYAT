-- Database schema for Al-Turath

CREATE DATABASE IF NOT EXISTS alkhayat_db;
USE alkhayat_db;

-- Users table (Customers, Tailors, Admins)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('customer', 'tailor', 'admin') DEFAULT 'customer',
    display_picture VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tailor Profiles
CREATE TABLE IF NOT EXISTS tailor_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    bio TEXT,
    location_lat DECIMAL(9,6),
    location_lng DECIMAL(9,6),
    rating DECIMAL(2,1) DEFAULT 0.0,
    portfolio_images JSON, -- Store as JSON array of URLs
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Clothing Categories (Dishdasha, Jellabiya, etc.)
CREATE TABLE IF NOT EXISTS clothing_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2)
);

-- Customization Options (Fabric, Colors, etc.)
CREATE TABLE IF NOT EXISTS customization_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    option_name VARCHAR(100) NOT NULL, -- 'Fabric', 'Color', 'Buttons'
    option_value VARCHAR(100) NOT NULL, -- 'Silk', 'White', 'Plastic'
    extra_price DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (category_id) REFERENCES clothing_categories(id) ON DELETE CASCADE
);

-- Measurements
CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    chest DECIMAL(5,2),
    waist DECIMAL(5,2),
    arm_length DECIMAL(5,2),
    shoulder_width DECIMAL(5,2),
    manual_input BOOLEAN DEFAULT TRUE,
    ai_assisted BOOLEAN DEFAULT FALSE,
    body_images JSON, -- Store AI-assisted measurement image paths
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Orders
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    tailor_id INT NOT NULL,
    category_id INT NOT NULL,
    customizations JSON,
    measurement_id INT NOT NULL,
    status ENUM('pending', 'accepted', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    progress_percentage INT DEFAULT 0,
    total_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id),
    FOREIGN KEY (tailor_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES clothing_categories(id),
    FOREIGN KEY (measurement_id) REFERENCES measurements(id)
);

-- Reviews
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    tailor_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (customer_id) REFERENCES users(id),
    FOREIGN KEY (tailor_id) REFERENCES users(id)
);
