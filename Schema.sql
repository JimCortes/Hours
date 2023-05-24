CREATE SCHEMA IF NOT EXISTS time_tracker;

CREATE TABLE IF NOT EXISTS time_tracker.employer (
    employer_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    employer_name VARCHAR(255) NOT NULL,
    employer_description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS time_tracker.wage_history (
    id_wage_history INT AUTO_INCREMENT PRIMARY KEY,
	employer_id INT NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    wage DECIMAL(5,2) NOT NULL,
	FOREIGN KEY (employer_id) REFERENCES time_tracker.employer(employer_id)
);

CREATE TABLE IF NOT EXISTS time_tracker.time_entries (
    time_id INT PRIMARY KEY AUTO_INCREMENT,
    employer_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    FOREIGN KEY (employer_id) REFERENCES time_tracker.employer(employer_id)
);

CREATE TABLE IF NOT EXISTS time_tracker.jobs (
    job_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    employer_id INT NOT NULL,
    day_id INT NOT NULL,
    time_entry DATETIME NOT NULL,
    job_number VARCHAR(255) NOT NULL,
    employees INT NOT NULL,
    tip DECIMAL(5,2) NOT NULL,
    job_description VARCHAR(255),        
    FOREIGN KEY (employer_id) REFERENCES time_tracker.employer(employer_id),
    FOREIGN KEY (day_id) REFERENCES time_tracker.time_entries(time_id)
);


CREATE TABLE IF NOT EXISTS time_tracker.users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_name VARCHAR(50) NOT NULL,
  user VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL
);

INSERT INTO users (user_name, user, password_hash)
VALUES ('Jimmy','Jim','$2b$12$YOEhpd7xrFqdVmthXCk5sOHTKs0Gq8T63FGN9MLPGbeksp3AK4/P.');



CREATE VIEW time_tracker.working_hours AS
SELECT 
    employer_id, 
    start_time, 
    end_time, 
    TIMESTAMPDIFF(MINUTE, start_time, end_time) / 60 as total_hours,
    CASE
        WHEN TIMESTAMPDIFF(MINUTE, start_time, end_time) / 60 > 8 
        THEN 8 
        ELSE TIMESTAMPDIFF(MINUTE, start_time, end_time) / 60
    END as first_8_hours,
    CASE
        WHEN TIMESTAMPDIFF(MINUTE, start_time, end_time) / 60 > 8 
        THEN TIMESTAMPDIFF(MINUTE, start_time, end_time) / 60 - 8 
        ELSE 0 
    END as after_8_hours
FROM time_entries;


