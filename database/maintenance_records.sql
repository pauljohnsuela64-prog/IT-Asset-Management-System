CREATE TABLE IF NOT EXISTS maintenance_records (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,

    asset_id INT NOT NULL,

    maintenance_date DATE NOT NULL,
    maintenance_type VARCHAR(50) NOT NULL,

    issue_description TEXT NOT NULL,
    action_taken TEXT DEFAULT NULL,

    technician_vendor VARCHAR(150) DEFAULT NULL,

    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,

    status VARCHAR(30) NOT NULL DEFAULT 'Open',

    completed_date DATE DEFAULT NULL,

    notes TEXT DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_maintenance_asset
        FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id)
);