import json
import unittest
from unittest.mock import patch
import server


class CatalogTests(unittest.TestCase):
    def test_common_codes(self):
        for code in ('I21.9', 'I26.9', 'J18.9'):
            self.assertTrue(server.validate_code(code)['valido'])
            self.assertTrue(server.validate_code(code)['descripcion'])

    def test_normalization(self):
        self.assertEqual(server.validate_code(' i219 ')['codigo'], 'I21.9')

    def test_unknown_and_invalid(self):
        for code in ('XYZ', 'I21.99', '', None, 'J18;DROP', 'Z99.7'):
            self.assertFalse(server.validate_code(code)['valido'])

    def test_catalog_size(self):
        self.assertEqual(len(server.catalog()), 11008)


class ContractTests(unittest.TestCase):
    def result(self):
        return {'resumen': 'Caso ficticio', 'codigos': [{'codigo': 'i219', 'evidencia': 'infarto', 'explicacion': 'Consignado'}],
                'preguntas': [{'pregunta': f'Pregunta {i}', 'respuesta': 'Respuesta'} for i in range(3)], 'limitaciones': []}

    def test_catalog_description_over_model(self):
        data=self.result()
        data['codigos'][0]['descripcion']='texto inventado'
        result=server.parse_result(json.dumps(data))
        self.assertEqual(result['codigos'][0]['codigo'], 'I21.9')
        self.assertEqual(result['codigos'][0]['descripcion'], server.catalog()['I21.9'])

    def test_invalid_code_visible_as_unvalidated(self):
        data=self.result();data['codigos'][0]['codigo']='NO-EXISTE'
        code=server.parse_result(json.dumps(data))['codigos'][0]
        self.assertFalse(code['valido']);self.assertIsNone(code['codigo'])
        self.assertEqual(code['codigo_propuesto'],'NO-EXISTE')

    def test_fenced_json(self):
        self.assertEqual(len(server.parse_result('```json\n'+json.dumps(self.result())+'\n```')['preguntas']),3)

    def test_incomplete_or_invalid_output(self):
        for data in ('nada', '[]', '{}', '{"resumen":"a","codigos":[],"preguntas":[],"limitaciones":[]}'):
            with self.assertRaises(ValueError):server.parse_result(data)

    def test_accented_field_label(self):
        data=self.result();item=data['codigos'][0]
        item['explicación']=item.pop('explicacion')
        self.assertEqual(server.parse_result(json.dumps(data))['codigos'][0]['explicacion'],'Consignado')

    def test_ambiguous_duplicate_labels_rejected(self):
        data=self.result();data['codigos'][0]['explicación']='Otro valor'
        with self.assertRaises(ValueError):server.parse_result(json.dumps(data))

    def test_empty_codes_allowed(self):
        data=self.result();data['codigos']=[]
        self.assertEqual(server.parse_result(json.dumps(data))['codigos'],[])

    def test_input_rejections(self):
        for data in ({}, [], {'texto':'a'*12001}, {'imagen':'data:image/jpeg;base64,YWJj'}, {'imagen':'data:text/html;base64,YWJj'}):
            with self.assertRaises(ValueError):server.validate_input(data)

    def test_text_input(self):
        self.assertEqual(server.validate_input({'texto':' ejemplo '}),('ejemplo',None))

    def test_missing_key(self):
        with patch.dict('os.environ',{},clear=True):
            with self.assertRaises(RuntimeError):server.analyze({'texto':'Caso educativo'})


if __name__ == '__main__':
    unittest.main()
