import asyncio

async def timeout_handler(async_func, timeout_seconds = 1):
    try:
        # Wait for the async function with a timeout
        await asyncio.wait_for(async_func(), timeout=timeout_seconds)
        print("Operation finished within the timeout.")
    except asyncio.TimeoutError:
        print("Timeout! Operation took too long.")
        
def timeout(async_func, timeout_seconds = 1):
    asyncio.create_task(timeout_handler(async_func, timeout_seconds))