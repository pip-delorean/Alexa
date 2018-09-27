import asyncio
from alexa_communicator import Alexa_Communicator as ac

alexa = ac()

loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(alexa.run())
    loop.run_forever()

except KeyboardInterrupt:
    pass

finally:
    print('Loop complete')
    loop.close()