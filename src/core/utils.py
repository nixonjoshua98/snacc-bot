from __future__ import annotations

from typing import Union

from defectio import Server


def get_server_id(server: Union[Server, str]) -> str:
    """ Defectio has 'message.server' type hinted as str, so we have this temporary check """
    if isinstance(server, Server):
        return server.id
    return server
