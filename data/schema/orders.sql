CREATE TABLE IF NOT EXISTS orders
(
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id      INTEGER  NOT NULL,
    total_amount     DECIMAL,
    currency         TEXT     NOT NULL,
    status           TEXT     NOT NULL DEFAULT 'created',
    shipping_address TEXT     NOT NULL,
    payment_status   TEXT     NOT NULL,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers (id)
);