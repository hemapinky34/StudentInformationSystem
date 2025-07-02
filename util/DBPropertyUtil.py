import os
import configparser


class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file):
        try:
            config = configparser.ConfigParser()
            # Get absolute path to properties file
            prop_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__),
                '..',
                property_file
            ))

            #print(f"Looking for config at: {prop_path}")  # Debug output

            if not os.path.exists(prop_path):
                raise FileNotFoundError(f"DB config file not found at: {prop_path}")

            with open(prop_path) as f:
                config.read_file(f)

            if not config.has_section('database'):
                raise ValueError("Missing [database] section in config file")

            return {
                'host': config.get('database', 'host', fallback='localhost'),
                'database': config.get('database', 'database'),
                'user': config.get('database', 'user'),
                'password': config.get('database', 'password')
            }
        except Exception as e:
            print(f"Error reading DB config: {str(e)}")
            raise