import logging
from datetime import date
from socketserver import BaseRequestHandler, UDPServer

# This is a simple syslog implementation which is written to test simple things quickly.

# Default syslog filename, the date indicates the date of the log.
LOG_FILE_NAME = f"syslog-{date.today().isoformat()}.log"

# Custom logger setup, I added filehandler to log to file, and streamhandler to display on console.
log_format = logging.Formatter(
    fmt="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)
log.propagate = False
log.setLevel(logging.INFO)
if not log.hasHandlers():
    file_handler = logging.FileHandler(LOG_FILE_NAME)
    file_handler.setFormatter(log_format)
    log.addHandler(file_handler)
    log_on_console = logging.StreamHandler()
    log_on_console.setFormatter(log_format)
    log.addHandler(log_on_console)


class SyslogHandler(BaseRequestHandler):
    """
    Server handler is required to handle udp request.
    See examples: https://www.programcreek.com/python/example/73643/SocketServer.BaseRequestHandler
    """
    def handle(self):
        data = self.request[0].strip().decode("utf-8")
        log.info(f"{self.client_address[0]}: {str(data)}")


if __name__ == "__main__":
    try:
        syslog = UDPServer(("0.0.0.0", 514), SyslogHandler)
        log.info("EZ syslog starts, CTRL-C to stop...")
        syslog.serve_forever(poll_interval=1)
    except KeyboardInterrupt:
        log.info("Ctrl-C detected, exit.")
