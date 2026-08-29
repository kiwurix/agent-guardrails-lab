CREATE TABLE IF NOT EXISTS customers
(
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name       TEXT NOT NULL,
    last_name        TEXT NOT NULL,
    email            TEXT NOT NULL UNIQUE,
    phone            TEXT UNIQUE,
    shipping_address TEXT,
    account_role     TEXT NOT NULL DEFAULT 'user'
);