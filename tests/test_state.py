import unittest
from src.core.state import StateManager

class TestStateManager(unittest.TestCase):
    def test_new_message(self):
        sm = StateManager()
        self.assertFalse(sm.is_duplicate('msg1'))
        self.assertFalse(sm.is_duplicate('msg2'))

    def test_duplicate_message(self):
        sm = StateManager()
        sm.is_duplicate('msg1')
        self.assertTrue(sm.is_duplicate('msg1'))

    def test_max_size(self):
        # Create manager with small size for testing
        sm = StateManager(max_size=2)
        
        sm.is_duplicate('msg1') # index 0
        sm.is_duplicate('msg2') # index 1
        sm.is_duplicate('msg3') # msg1 should be evicted
        
        # msg2 should still be in the list
        self.assertTrue(sm.is_duplicate('msg2'))
        # msg1 should become 'new' again as it was evicted
        self.assertFalse(sm.is_duplicate('msg1'))

if __name__ == '__main__':
    unittest.main()