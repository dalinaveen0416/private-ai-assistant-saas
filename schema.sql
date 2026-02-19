-- Create Database
CREATE DATABASE IF NOT EXISTS genai_saas;

USE genai_saas;


-- =========================
-- Users Table
-- =========================

CREATE TABLE IF NOT EXISTS users (

    id INT AUTO_INCREMENT PRIMARY KEY,

    email VARCHAR(255) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);


-- =========================
-- Documents Table
-- =========================

CREATE TABLE IF NOT EXISTS documents (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    filename VARCHAR(255),

    vector_path VARCHAR(255),

    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE

);


-- =========================
-- Chat History Table
-- =========================

CREATE TABLE IF NOT EXISTS chat_history (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    query TEXT,

    response TEXT,

    tokens_used INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE

);


-- =========================
-- Usage Tracking Table
-- =========================

CREATE TABLE IF NOT EXISTS usage_tracking (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL UNIQUE,

    query_count INT DEFAULT 0,

    token_usage INT DEFAULT 0,

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE

);