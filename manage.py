# TODO implement the module
import sys
import uvicorn

from backend.settings import SERVER_HOST, SERVER_PORT, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV


def main():
    if 'runserver' in sys.argv:
        uvicorn.run(
            'server:app',
            host=SERVER_HOST,
            port=SERVER_PORT,
            ssl_certfile=WEBHOOK_SSL_CERT,
            ssl_keyfile=WEBHOOK_SSL_PRIV,
            log_level='info'
        )


if __name__ == '__main__':
    main()
