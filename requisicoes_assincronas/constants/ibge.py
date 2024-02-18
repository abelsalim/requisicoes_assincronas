from types import SimpleNamespace

# Referente ao arquivo 'main.py'
ibge = SimpleNamespace()

ibge.get_names = 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
ibge.get_noticias = 'http://servicodados.ibge.gov.br/api/v3/noticias/'
ibge.get_ranking = (
    'https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking'
)

