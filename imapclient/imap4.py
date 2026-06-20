# Copyright (c) 2015, Menno Smits
# Released subject to the New BSD License
# Please see http://en.wikipedia.org/wiki/BSD_licenses

import imaplib
import socket
from typing import Optional


# class IMAP4WithTimeout(imaplib.IMAP4):
#     def __init__(self, address: str, port: int, timeout: Optional[float]) -> None:
#         self._timeout = timeout
#         imaplib.IMAP4.__init__(self, address, port)

#     def open(
#         self, host: str = "", port: int = 143, timeout: Optional[float] = None
#     ) -> None:
#         # This is overridden to make it consistent across Python versions.
#         self.host = host
#         self.port = port
#         self.sock = self._create_socket(timeout)
#         self.file = self.sock.makefile("rb")

#     def _create_socket(self, timeout: Optional[float] = None) -> socket.socket:
#         return socket.create_connection(
#             (self.host, self.port), timeout if timeout is not None else self._timeout
#         )


class IMAP4WithTimeout(imaplib.IMAP4):
    """
    IMAP4 class that supports connection timeouts.
    
    Modified for Python 3.14+ compatibility:
    - Removed custom 'open()' method which attempted to set a read-only 'file' property.
    - Ensured 'timeout' is passed to parent __init__ so imaplib handles socket creation correctly.
    """
    def __init__(self, host: str = '', port: int = 143, timeout: float | None = None) -> None:
        self._timeout = timeout
        # FIX: Pass timeout to parent so imaplib 3.14+ configures socket timers correctly
        super().__init__(host=host, port=port, timeout=timeout)

    def _create_socket(self, timeout: float | None = None) -> socket.socket:
        # Use the instance timeout if no specific timeout is provided
        effective_timeout = timeout if timeout is not None else self._timeout
        return socket.create_connection(
            (self.host, self.port), effective_timeout
        )