import unittest
import re
from db_anonymizer import sanitize_line

class TestDatabaseAnonymizer(unittest.TestCase):

    def setUp(self):
        # Initializing clean dynamic cache states for isolation
        self.cache_maps = {
            "emails": {},
            "phones": {}
        }

    def test_email_sanitization(self):
        raw_sql = "INSERT INTO users VALUES (1, 'alex', 'real-email@domain.com');"
        result = sanitize_line(raw_sql, self.cache_maps)
        
        # Verify original email is completely gone
        self.assertNotIn("real-email@domain.com", result)
        # Verify fallback mock mask pattern exists
        self.assertTrue(re.search(r'user_\d+@', result))

    def test_credit_card_sanitization(self):
        raw_sql = "INSERT INTO billing VALUES (101, '4111222233334444');"
        result = sanitize_line(raw_sql, self.cache_maps)
        
        # Verify real card number sequence is obliterated
        self.assertNotIn("4111222233334444", result)
        self.assertIn("4111-XXXX-XXXX-", result)

    def test_data_consistency(self):
        # If the same email appears twice, it must get the exact same mask
        line1 = "INSERT INTO logs VALUES ('test@domain.com');"
        line2 = "INSERT INTO users VALUES ('test@domain.com');"
        
        res1 = sanitize_line(line1, self.cache_maps)
        res2 = sanitize_line(line2, self.cache_maps)
        
        email_mask1 = re.search(r'user_\d+@[a-z.]+', res1).group(0)
        email_mask2 = re.search(r'user_\d+@[a-z.]+', res2).group(0)
        
        self.assertEqual(email_mask1, email_mask2)

if __name__ == '__main__':
    unittest.main()
