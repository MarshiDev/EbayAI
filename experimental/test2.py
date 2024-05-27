from gradio_client import Client
import asyncio


async def get_response(client, message):
    result = await client.predict(
        message,
        0.95,
        512,
        api_name="/chat"
    )
    return result.lstrip("assistant\n")


async def main():
    client = Client("ysharma/Chat_with_Meta_llama3_8b")
    messages = [
        "Hi, whats your name?",
        "Tell me a fun fact.",
        "What's the weather like today?",
        "Explain quantum mechanics in simple terms."
    ]

    tasks = [get_response(client, message) for message in messages]
    responses = await asyncio.gather(*tasks)

    for i, response in enumerate(responses):
        print(f"Response to '{messages[i]}':\n{response}\n")

if __name__ == "__main__":
    asyncio.run(main())
