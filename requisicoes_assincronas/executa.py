from asyncio import run, gather

from constants.ibge import ibge
from models.requisicao import RequisicaoAsync


async def main():
    async with RequisicaoAsync() as request:

        retorno = await gather(
            request.cliente(
                retorno='json',
                content_type='application/josn',
                timeout=10,
                **{'url': ibge.get_ranking}
            )
        )

        for conteudo in retorno:
            print(conteudo)


run(main())