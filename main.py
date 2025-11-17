import asyncio
from myapp.data.storage import init_db

from myapp.core.pula_entrance import run_entrance_simulation_pula
from myapp.core.rijeka_entrance import run_entrance_simulation_rijeka
from myapp.core.umag_entrance import run_entrance_simulation_umag
from myapp.core.camera1 import run_camera1_simulation
from myapp.core.camera2 import run_camera2_simulation
from myapp.core.pula_exit import run_pula_exit_simulation
from myapp.core.rijeka_exit import run_rijeka_exit_simulation
from myapp.core.umag_exit import run_umag_exit_simulation
from myapp.core.restarea1 import run_restarea1_simulation
from myapp.core.restarea2 import run_restarea2_simulation

async def main():
    init_db()

    tasks = [
        asyncio.create_task(run_entrance_simulation_pula()),
        asyncio.create_task(run_entrance_simulation_rijeka()),
        asyncio.create_task(run_entrance_simulation_umag()),
        asyncio.create_task(run_camera1_simulation()),
        asyncio.create_task(run_camera2_simulation()),   
        asyncio.create_task(run_pula_exit_simulation()),
        asyncio.create_task(run_rijeka_exit_simulation()),
        asyncio.create_task(run_umag_exit_simulation()),
        asyncio.create_task(run_restarea1_simulation()),
        asyncio.create_task(run_restarea2_simulation()),
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
