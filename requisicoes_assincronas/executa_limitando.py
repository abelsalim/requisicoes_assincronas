import asyncio


async def limitador(lista, limite):
    semaphore = asyncio.Semaphore(limite)

    async def interno(item):
        async with semaphore:
            print(f'Semaphore Value: {semaphore._value}')
            await asyncio.sleep(1)
            print(f'Item Lista: {item}')

            return item

    lista_retorno = []

    for indice in range(0, len(lista), limite):
        faixa = lista[indice: indice + limite]

        # Usando asyncio.gather para paralelizar as chamadas a interno
        lista_retorno.extend(
            await asyncio.gather(*[interno(item) for item in faixa])
        )

    return lista_retorno


async def main():
    retorno = [item for item in await limitador([1, 2, 4, 5, 6, 7, 8, 9], 2)]

    print(retorno)


asyncio.run(main())
