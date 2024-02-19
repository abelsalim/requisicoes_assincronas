
from types import SimpleNamespace

requisicao = SimpleNamespace()

# Relacionados aos parâmetros repassados em 'cliente'
requisicao.kwargs = ['url', 'json' , 'params']
requisicao.tipos_retorno = [
    'text', 'read' , 'json', 'status', 'reason', 'response'
]
requisicao.tipos_metodos = [
    'get', 'post', 'put', 'delete', 'head', 'options', 'patch'
]

requisicao.lista_comparativa = [
    requisicao.tipos_metodos,
    requisicao.tipos_retorno
]

# Relacionados aos tipo
requisicao.tipo_metodo_retorno = 'method'
requisicao.retorne_json = 'json'
requisicao.retorne_response = 'response'

# Relacionados aos 'erros'
requisicao.parametro_invalido = 'Parâmetro "{valor}" não reconhecido.'
