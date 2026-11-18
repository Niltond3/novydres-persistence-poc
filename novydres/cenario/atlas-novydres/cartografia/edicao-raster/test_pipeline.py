"""Testes mínimos de integridade raster: python -m unittest test_pipeline.py"""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from PIL import Image

spec = importlib.util.spec_from_file_location('pipeline', Path(__file__).parent/'pipeline.py')
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)

class TestPipeline(unittest.TestCase):
    def test_mask_and_pixel_preservation(self):
        src = Image.new('RGB', (10,10), (9,40,130))
        edit = Image.new('RGB', (10,10), (210,80,30))
        mask = pipeline.mask_from_spec({
            'base':{'size':[10,10]},
            'polygons':[[[2,2],[7,2],[7,7],[2,7]]],
            'protected_holes':[[[4,4],[5,4],[5,5],[4,5]]]
        }, (10,10))
        with tempfile.TemporaryDirectory() as d:
            output = pipeline.compose(src, edit, mask, Path(d)/'out.png')
            report = pipeline.verify(src, output, mask)
            self.assertEqual(report['outside_changes'], 0)
            self.assertEqual(report['inside_changes'], report['mask_pixels'])
            self.assertEqual(output.getpixel((0,0)), src.getpixel((0,0)))
            self.assertEqual(output.getpixel((4,4)), src.getpixel((4,4)))
            self.assertEqual(output.getpixel((3,3)), edit.getpixel((3,3)))
            file = Path(d)/'compare.html'
            pipeline.comparator(src, output, file, (1,1,9,9))
            html = file.read_text()
            for label in ('Mapa completo','Lado a lado','Deslizar','Detalhe','data:image/webp;base64,'):
                self.assertIn(label, html)
            self.assertNotIn('__A__', html)

    def test_size_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            pipeline.mask_from_spec({'base':{'size':[12,10]},'polygons':[]},(10,10))

if __name__=='__main__': unittest.main()
