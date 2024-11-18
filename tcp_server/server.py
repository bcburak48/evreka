import asyncio
import json
from celery_app.tasks import process_data


async def handle_client(reader, writer):
    data = await reader.read(1024)
    message = data.decode()
    try:
        # Assuming data is in JSON format
        data_dict = json.loads(message)
        process_data.delay(data_dict)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON received: {e}")
    finally:
        writer.close()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8888)
    print("TCP server running on port 8888")
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
