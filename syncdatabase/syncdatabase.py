from consume_messages_user import consume_messages_user
from consume_messages_imageprofile import consume_messages_imageprofile
from consume_messages_userprofile import consume_messages_userprofile
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

if __name__ == '__main__':
    # Start consuming messages
    try:
        print('Start consuming messages...')
        executor.submit(consume_messages_user)
        executor.submit(consume_messages_imageprofile)
        executor.submit(consume_messages_userprofile)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
    except Exception as e:
        print('Error consuming messages:', e)

    # Wait for the executor to finish
    executor.shutdown(wait=True)