CREATE TABLE IF NOT EXISTS asset_assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,

    asset_id INT NOT NULL,
    employee_id INT NOT NULL,

    assigned_date DATE NOT NULL,
    returned_date DATE DEFAULT NULL,

    status VARCHAR(20) NOT NULL DEFAULT 'Assigned',

    notes TEXT DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_assignment_asset
        FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id),

    CONSTRAINT fk_assignment_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);