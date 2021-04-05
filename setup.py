import motor.motor_asyncio

#set up database for the server
async def setup():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.rabbitmq_monitor
    return db
    