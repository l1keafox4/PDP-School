import asyncio
import aiogram
import asyncpg
from asyncpg import Pool

# Initialize bot
bot = aiogram.Bot(token="6944180673:AAE7pdH36HaanXrGUejIOAJOq-N-EtQgtxs")
dp = aiogram.Dispatcher(bot)

# PostgreSQL database configuration
DB_USER = 'postgres'
DB_PASSWORD = '1234'
DB_NAME = 'products'
DB_HOST = 'localhost'

# Create a connection pool
async def create_pool():
    return await asyncpg.create_pool(user=DB_USER, password=DB_PASSWORD,
                                     database=DB_NAME, host=DB_HOST)

# Command handler for /find
@dp.message_handler(commands=['find'])
async def find_product(message: aiogram.types.Message):
    try:
        # Extract product name from user message
        product_name = message.get_args()

        # Fetch product information from the database
        async with pool.acquire() as connection:
            query = "SELECT * FROM products WHERE name ILIKE $1"
            products = await connection.fetch(query, f"%{product_name}%")

            # If products are found, send their information to user
            if products:
                for product in products:
                    await message.answer(f"Product: {product['name']}\nDescription: {product['description']}")
            else:
                await message.answer("No products found.")

    except Exception as e:
        print(f"Error: {e}")

# Main function to start the bot
async def main():
    try:
        # Create a connection pool
        global pool
        pool = await create_pool()

        # Start the bot
        await dp.start_polling()

    finally:
        # Close the connection pool when shutting down
        await pool.close()

if __name__ == '__main__':
    asyncio.run(main())
