import os
import uvicorn
from fastapi import FastAPI
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from mcp.server.sse import SseServerTransport
from x_twitter_mcp.server import server


app = FastAPI()

# Standard FastAPI middleware works completely fine here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id", "mcp-protocol-version"],
)

sse = SseServerTransport("/")

# 1. Define raw ASGI apps that receive the raw scope, receive, and send components
async def handle_sse(scope, receive, send):
    async with sse.connect_sse(scope, receive, send) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
server._mcp_server.create_initialization_options()
        )

async def handle_messages(scope, receive, send):
    await sse.handle_post_message(scope, receive, send)

# 2. Directly inject them into the low-level router to bypass FastAPI's response wrapper
app.mount("/sse", handle_sse)
app.mount("/messages", handle_messages)

def main():
    port = int(os.environ.get("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
