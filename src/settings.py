from starlette.config import Config

config = Config(".env")

LOGGER_FOLDER = config("LOGGER_FOLDER", cast=str, default="src/logs/")
AIVEN_KAFKA_WEBSITE_TOPIC = "website-status"
BOOTSTRAP_SERVER = "status-check-ravi9235705910-586e.aivencloud.com:25006"
FOLDER_PATH = "/Users/nirjharijankar/Downloads/"
SSL_CAFILE = FOLDER_PATH + "ca_aiven.pem"
SSL_CERTFILE = FOLDER_PATH + "service.cert"
SSL_KEYFILE = FOLDER_PATH + "service.key"
DB_URI = "postgres://avnadmin:AVNS_MSSWiAJuI5-prPMTh8j@pg-39d8773b-ravi9235705910-586e.aivencloud.com:25004/defaultdb?sslmode=require"  # noqa: E501
TIMEOUT = 20
