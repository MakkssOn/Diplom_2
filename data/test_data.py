import uuid

class TestData:
    @staticmethod
    def unique_user():
        return {
            "email": f"{uuid.uuid4()}@example.com",
            "password": "securePassword123",
            "name": "TestUser"
        }

    @staticmethod
    def persistent_user():
        return {
            "email": "persistent_user@example.com",
            "password": "securePassword123",
            "name": "PersistentUser"
        }
