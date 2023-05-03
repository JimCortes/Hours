CREATE SCHEMA IF NOT EXISTS time_tracker

CREATE TABLE IF NOT EXISTS time_tracker.employer (
    employer_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    employer_name VARCHAR(255) NOT NULL,
    employer_description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS time_tracker.wage_history (
    id_wage_history INT AUTO_INCREMENT PRIMARY KEY,
    employer_id INT FOREIGN KEY REFERENCES time_tracker.employer(employer_id) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME,
    wage DECIMAL(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS time_tracker.time_entries (
    time_id INT PRIMARY KEY AUTO_INCREMENT,
    employer_id INT FOREIGN KEY REFERENCES time_tracker.employer(employer_id) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
);

CREATE TABLE IF NOT EXISTS time_tracker.jobs (
    job_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    employer_id INT FOREIGN KEY REFERENCES time_tracker.employer(employer_id) NOT NULL,
    day_id INT FOREIGN KEY REFERENCES time_tracker.time_entries(time_id) NOT NULL,
    time_entry DATETIME NOT NULL,
    job_number VARCHAR(255) NOT NULL,
    employees INT NOT NULL,
    tip DECIMAL(5,2) NOT NULL,
    job_description VARCHAR(255)        
);





