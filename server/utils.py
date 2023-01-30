import os
import asyncio


def env_bool(param: str, defval=None) -> bool:
    val = os.getenv(param, defval)
    return bool(val and val != "0" and val.lower() != "false")


def is_int(val):
    return isinstance(val, int) or (isinstance(val, str) and val.isdigit())


async def run_thread(fn, *args):
    return await asyncio.get_event_loop().run_in_executor(None, fn, *args)
