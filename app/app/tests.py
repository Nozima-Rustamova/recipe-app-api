"""Sample tests"""

from django.test import SimpleTestCase

from app import calc

class ClacTests(SimpleTestCase):
    """Tests case"""
    
    def test_add_numbers(self):
        """test numbers together"""
        res=calc.add(5, 6)
        
        self.assertEqual(res, 11)
        
    def test_subtract_numbers(self):
        """Test substercting numbers"""
        res=calc.subtract(10, 5)
        
        self.assertEqual(res, 5)
        