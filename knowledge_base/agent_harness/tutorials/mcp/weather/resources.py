from mcp.server import Server
from mcp import types
from  mcp.server.stdio import stdio_server
import asyncio
import urllib.parse


app = Server("example-server")

import os
PWD = os.getcwd()

@app.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri=f"file:///{path}",
            name=path,
            mimeType="text/plain"
        )
        for path in os.listdir(PWD)
    ]

@app.read_resource()
async def read_resource(uri) -> str:
    return open(PWD + "/" + str(uri).replace("file:///", "")).read()

# Start server
async def run():
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(run())