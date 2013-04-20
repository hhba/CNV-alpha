# coding: utf-8
# Generar data para el D3 Sankey
# autor: Manuel Aristarán <http://jazzido.com>
import requests
import simplejson

URL = 'https://www.googleapis.com/fusiontables/v1/query'
TABLE_ID = '19VO5zihUNJAK2xa7_4f2R3FuC-SgJD0pzI8UCjg'
API_KEY = 'AIzaSyAm9yWCV7JPCTHCJut8whOjARd7pwROFDQ'

def generate():
    rv = { 
        'nodes': [],
        'links': [] 
    }

    nodes = ('Fuerza interviniente', 'Represor', 'Empresario', 'Empresa')

    for n in nodes:
        query = 'SELECT \'%s\' from %s' % (n, TABLE_ID)
        r = requests.post(URL,
                          data={'sql': query,
                                'key': API_KEY })
        rv['nodes'] = rv['nodes'] + [x[0] for x in r.json()['rows'] if x[0] != '']

    rv['nodes'] = [{'name': x} for x in list(set(rv['nodes']))]

    links = (('Fuerza interviniente', 'Represor'), 
             ('Represor', 'Empresario'), 
             ('Empresario', 'Empresa'))

    for l in links:
        query = 'SELECT COUNT(), \'%s\', \'%s\' FROM %s GROUP BY \'%s\', \'%s\'' % (l[0], l[1], TABLE_ID, l[0], l[1])

        r = requests.post(URL,
                          data={
                              'sql': query,
                              'key': API_KEY })

        rv['links'] = rv['links'] + [{'source': rv['nodes'].index({'name': x[1]}), 
                                      'target': rv['nodes'].index({'name': x[2]}), 
                                      'value': int(x[0])} 
                                     for x in r.json()['rows']]
    

    return rv

if __name__ == '__main__':
    r = generate()
    print simplejson.dumps(r)
