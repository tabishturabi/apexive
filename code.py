import xmlrpc.client
import csv

class OdooCustomerImporter:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password

    def connect_to_odoo(self):
        """
        Establishes a connection to the Odoo instance.

        Returns:
            common (ServerProxy): The common object for the Odoo instance.
            models (ServerProxy): The models object for the Odoo instance.
            uid (int): The user ID for authentication.
        """
        common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        uid = common.authenticate(self.db, self.username, self.password, {})
        models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        return common, models, uid

    def import_customers(self, csv_file_path):
        """
        Imports customers from a CSV file into Odoo.

        Args:
            csv_file_path (str): The path to the CSV file containing customer data.

        Returns:
            bool: True if the import is successful, False otherwise.
        """
        try:
            common, models, uid = self.connect_to_odoo()

            # Read customer data from the CSV file
            with open(csv_file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                customer_data = list(reader)

            # Create customers in Odoo
            for customer in customer_data:
                partner_id = models.execute_kw(self.db, uid, self.password, 'res.partner', 'create', [{
                    'name': customer['name'],
                    'email': customer['email'],
                    'phone': customer['phone'],
                    # Add more customer fields as needed
                }])

                if partner_id:
                    print(f"Customer '{customer['name']}' imported with ID: {partner_id}")
                else:
                    print(f"Failed to import customer '{customer['name']}'")

            return True

        except Exception as e:
            print(f"Error importing customers: {e}")
            return False

# Example usage
url = "https://your-odoo-instance.com"
db = "your_database"
username = "admin"
password = "your_password"
csv_file_path = "customers.csv"

customer_importer = OdooCustomerImporter(url, db, username, password)
success = customer_importer.import_customers(csv_file_path)

if success:
    print("Customers imported successfully.")
else:
    print("Failed to import customers.")
