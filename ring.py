import asyncio
import functools

async def run(from_queue, next_queue):
  while 1:
    data = await from_queue.get()
    print('Data received: {}'.format(data))
    asyncio.async(next_queue.put(num))

def main():
  loop = asyncio.get_event_loop()
  queue = asyncio.Queue()
  first_queue = queue
  try:
    for i in range(5):
      next_queue = asyncio.Queue()
      print("gogin to deadlockl...")
      loop.run_until_complete(run(queue, next_queue))
      queue = next_queue
    asyncio.async(first_queue.put(num))
  finally:
    loop.close()

main()
