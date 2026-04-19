#!/bin/bash

DATABASE="sales"

# Disable foreign key checks
mysql -e "SET FOREIGN_KEY_CHECKS=0;" "$DATABASE"

# Truncate all tables
mysql -Nse "SHOW TABLES" "$DATABASE" | while read table; do
    mysql -e "TRUNCATE TABLE \`$table\`;" "$DATABASE"
done

# Re-enable foreign key checks
mysql -e "SET FOREIGN_KEY_CHECKS=1;" "$DATABASE"

echo "All tables truncated successfully."