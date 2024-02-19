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

## Limitadores

Ao trabalhar com requisições assíncronas é necessário limitar do lado cliente a
quantidade de requisições simultâneas, visto que o código pode ser aplicado em
um ORM que possui diversos usuários que alimentam um e-commerce por exemplo.

Sabendo disso, dois limitadores foram aplicados, o `limit_connector` repassado
ao instanciar o contexto assíncrono `with` como atributo de `RequisicaoAsync` e
também o `limit` existente em no método `limitador` de `RequisicaoAsync`.

### 1º caso: `limit_connector`

Ao instanciar a classe  `RequisicaoAsync`, o contexto gera um conector que
recebe o parâmetro `limit_connector` e o agrega como valor ao parâmetro `limit`
de `aiohttp.TCPConnector`. Esta última classe, por sua vez, possibilita gerar
conectores customizáveis.

```python
async def __aenter__(self):
    # Gera connector com limite de conexão preestabelecido
    self.conector = aiohttp.TCPConnector(limit=self.limit_connector)
    # Gera session
    self.session = aiohttp.ClientSession(connector=self.conector)

    return self
```

O parâmetro `limit` do `aiohttp.TCPConnector` tem a função de impor um limite
com proporções globais nas solicitações em todo o sistema. Em outras palavras,
em um ambiente onde um ERP possui vários pontos de requisição distribuídos em
diversas funcionalidades internas, apenas será possível realizar um certo número
de solicitações simultâneas.

### 2º caso: `limit` de `limitador`

O método `limitador`  do `RequisicaoAsync` possui um controle interno sobre as
solicitações feitas em um escopo local. Em outras palavras, dentro do meu
método, posso restringir a execução para 50 solicitações simultâneas em um
escopo de 1.000 tarefas, enquanto o meu limite global - `limit_connector` - está
configurado para permitir apenas 100 requisições simultâneas, por exemplo.

```python
from asyncio import create_task

from models.requisicao import RequisicaoAsync


async def mostra_numero(numero):
    return numero


async def main():
    async with RequisicaoAsync(limit_connector=100) as request:
        lista_numeros = [
            create_task(mostra_numero(numero)) for numero in range(1, 10)
        ]

        retorno = [
            item for item in await request.limitador(
                tasks=lista_numeros,
                limit=2
            )
        ]

        print(retorno)
```

Ao executar a função `main` o retorno obtido é simplesmente a lista gerada:
[1, 2, 3, 4, 5, 6, 7, 8, 9].

Para um segundo exemplo e melhor compreensão do funcionamento, vamos adicionar
"prints" ao método `interno` dentro de `limitador`, e poderemos acompanhar o
processo.

```python
async def interno(task):
    # Aplicando delimitação do semaphore
    async with semaphore:
        print(f'Semaphore Value: {semaphore._value}')
        await sleep(0.00001)
        print(f'Item Lista: {task._result}')
        
        return await task
```

Ao executar o `main` o resultado será:

```bash
Semaphore Value: 1
Semaphore Value: 0
Item Lista: 1
Item Lista: 2
Semaphore Value: 1
Semaphore Value: 0
Item Lista: 3
Item Lista: 4
Semaphore Value: 1
Semaphore Value: 0
Item Lista: 5
Item Lista: 6
Semaphore Value: 1
Semaphore Value: 0
Item Lista: 7
Item Lista: 8
Semaphore Value: 1
Item Lista: 9
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

O retorno indica que o semaphore é zerado a cada 2 iterações. Este limite foi
repassado pelo parâmetro `limit`.

### Performance

Ao utilizarmos os limitadores  é notável um ganho de performance quando ambas as
limitações tem valores idênticos ou similares.

```bash
➜ python requisicoes_assincronas/executa.py
- limit connector: 10
- limit limitador: 10
- len tasks: 10
- tempo execução: 1.504553

➜ python requisicoes_assincronas/executa.py
- limit connector: 100
- limit limitador: 10
- len tasks: 100
- tempo execução: 4.437354

➜ python requisicoes_assincronas/executa.py
- limit connector: 100
- limit limitador: 100
- len tasks: 100
- tempo execução: 1.606592
```

## Conclusão - Parte 2

Os limites estabelecidos podem ter escopo globais ou locais, onde ambos podem
impactar de forma positiva ou negativa em seu ambiente.
