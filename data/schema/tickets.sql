CREATE TABLE IF NOT EXISTS tickets
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER  NOT NULL,
    order_id    INTEGER,
    status      TEXT     NOT NULL DEFAULT 'open',
    subject     TEXT     NOT NULL,
    body        TEXT     NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (order_id) REFERENCES orders (id)
);