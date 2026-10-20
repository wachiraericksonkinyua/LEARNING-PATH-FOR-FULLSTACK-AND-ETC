import asyncio
import time

def sync_function(test_param: str) -> str:
    print("This is a synchronous function")

    time.sleep(3)
    return f"Sync rewrite: {test_param}"

#Also known as coroutines, they are defined with the async keyword and can be paused and resumed, allowing other tasks to run concurrently while waiting for I/O operations or other time-consuming tasks to complete.
async def async_function(test_param: str) -> str:
    print("This is an asynchronous function")

    await asyncio.sleep(3)
    return f"Async result: {test_param}"

async def main():
   """ sync_result = sync_function("test")
    print(sync_result)"""
   #loop = asyncio.get_running_loop()
   #future =loop.create_future()
   #print(f"Empty Future: {future}")

   #future.set_result("Future result: Test")
   #future_result = await future
   #print(future_result)
   
   #coroutine_obj= async_function("test")
   #print(f"Coroutine object: {coroutine_obj}")

   #coroutine_result = await coroutine_obj
   #print(f"Coroutine result: {coroutine_result}")

   task = asyncio.create_task(async_function("test"))
   print(f"Task created: {task}")

   task_result = await task
   print(f"Task result: {task_result}")

 
if __name__ == "__main__":
    asyncio.run(main())