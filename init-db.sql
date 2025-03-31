CREATE TABLE IF NOT EXISTS defects (
    defect INT PRIMARY KEY,
    status TEXT NOT NULL,
    history JSONB
);