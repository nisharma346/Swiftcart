from django.test import TestCase
from django.urls import reverse


class GalleryViewTests(TestCase):
    def test_gallery_page_renders(self):
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swiftcart/gallery.html')
