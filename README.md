# Sobre

Pensando sobre como utilizar `aiohttp` e suas funcionalidades, fiz essa classe
simples que pode facilitar o uso diário nas implementações em framworks
diversificados.

## Imports necessários

Os imports necessários para `aiohttp` serão os seguintes:

```python
import asyncio
import aiohttp
```

Os imports necessários para `RequisicaoAsync` serão os seguintes:

```python
from models.requisicao import RequisicaoAsync
```

## URL utilizado

Para exemplificação a seguir iremos utilizar a API do IBGE onde as variáveis
serão:

```python
GET_IBGE_RANKING= 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking'
```

## Forma de uso

### Request tipo GET por: `aiohttp`
```python
async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(GET_IBGE_RANKING) as response:
            print(response.status)
            print(await response.json())
```

Acima temos a função `main` que realiza a requisição `get` para obter o ranking
de nomes registrados pelo IBGE ao decorrer dos anos. Por fim, ao realizar o
`get` é 'printado' o status seguido do retorno JSON - data.

### Request tipo GET por: `RequisicaoAsync`
```python
async def main():
    async with RequisicaoAsync() as request:
        lista_retorno = await request.cliente(
            metodo='get',
            parametros_retorno=['status', 'json'],
            **{'url': GET_IBGE_RANKING}
        )

        for retorno in lista_retorno:
            print(retorno, end=f'\n{35 * "-"}\n')
```

Agora temos a implementação de `RequisicaoAsync` na função `main` onde o método
cliente recebe os parâmetros `metodo`, `parametros_retorno` e `kwargs`.

- __metodo__: Sugere ao método de requisição, como: get, post, put, delete e
etc.
- __parametros_retorno__:  Solicita as tipagens de retornos referentes ao
response, como:
    - __json__: Retorna o `json` caso possível;
    - __text__: Retorna o `text` caso possível;
    - __read__: Retorna uma `string` binaria caso possível;
    - __status__: Retorna o `status` da requisição;
    - __reason__: Retorna o `reason` da requisição;
    - __response__: Retorna o objeto `response`;
- __kwargs__: 
    - __url__: URL utilizada na conexão;
    - __params__: Parâmetros adicionados na URL de conexão;
    - __headers__: Dicionário que compõe o cabeçalho da conexão;
    - __json__: Dicionário que será tratado como JSON;
    - __data__: objetos do tipo `list`, `dict`, `binary` ou `str` que
    substituirão o payload;

> __Nota__: O retorno é uma lista que ira conter os dados solicitados em
> parametros_retorno.

## Conclusão - Parte 1

Essas são as funcionalidades básicas que atendem 90% das demandas necessárias no
dia-a-dia, porém casos adicionais como tratamento de `cookies` e `history` podem
ser facilmente adicionados na classe `RequisicaoAsync`em `models`.
