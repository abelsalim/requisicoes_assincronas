from datetime import datetime
from asyncio import run, create_task

from constants.ibge import ibge
from models.requisicao import RequisicaoAsync


async def main():
    async with RequisicaoAsync(limit_connector=100) as request:
        inicio = datetime.now()

        tasks = [
            create_task(
                request.cliente(
                    parametros_retorno=['json'],
                    content_type='application/josn',
                    timeout=100,
                    **{'url': ibge.get_ranking}
                )
            ) for _ in range(100)
        ]

        limit = 100

        retorno = await request.limitador(tasks=tasks, limit=limit)

        tempo = datetime.now() - inicio

        print(
            f'limit connector: {request.conector.limit}\n'
            f'limit limitador: {limit}\n'
            f'len tasks: {len(tasks)}\n'
            f'tempo execução: {tempo.total_seconds()}'
        )

        for conteudo in retorno[:3]:
            print(conteudo)

        '''
        A execução tem tempo de resultado superior quando o parâmetro limit do
        método limitador de request tem o mesmo valor que limit_connector.

        Exemplos:
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
        '''


run(main())