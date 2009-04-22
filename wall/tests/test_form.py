from django.test import TestCase
from wall.forms import WallItemForm

class TestWallItemForm(TestCase):
    
    def setUp(self):
        self.form = WallItemForm()
        
    def tearDown(self):
        pass
        
    def test_display_form(self):
        text = """<p><label for="id_posting">Item:</label> <textarea id="id_posting" rows="5" cols="50" name="posting"></textarea></p>"""
        self.assertEquals(self.form.as_p(),text)