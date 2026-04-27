in this module i created another database called sales and populated it wit a sql file
this was to create roles and introduce access manaand security onto the database.

---creating and populating the database using mysql CLI
CREATE DATABASE sales;
    SOURCE database_create_load.sql;

---the below is all done in phpmyadmin

---i then created 6 roles an admin role with all permissions an a analyst role with the below permissions
Viewing privileges for data
Structural privileges for creating and displaying views, temporary tables, and routines
No administrative privileges
---and a reprter role with SELECT permissions for data only.
---the final role is db_external with only SELECt permissions on all columns except amount in the FactSales
    tables.

---next we worked on encryption first i encrypted a passphrase below
SELECT SHA2('sales info encryption', 256);
+------------------------------------------------------------------+
| SHA2('sales info encryption', 256)                               |
+------------------------------------------------------------------+
| e7826d5764b270b972617204cfe9331ab7d93968f16bb55bead11a3df3fb0128 |

--- i then altered the amount column to be a variable binary column 
ALTER TABLE FactSales MODIFY amount VARBINARY(255);

---i then Encrypted the column using the passphrase from above
UPDATE FactSales SET amount = AES_ENCRYPT(amount, SHA2('sales info encryption', 255));

--- i then queried the data to get the first 5 rows to show the encryption
SELECT * FROM FactSales LIMIT 5;

---i then queried the data with decyption using the passphrase above
SELECT *, AES_DECRYPT(amount,SHA2('sales info encryption',256)) AS amount_decrypted FROM FactSales LIMIT 5;
