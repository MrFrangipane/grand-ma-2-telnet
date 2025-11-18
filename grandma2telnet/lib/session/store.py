import os

from grandma2telnet.lib.session import Session


class SessionStore:
    def __init__(self):
        pass

    def new(self) -> Session:
        return Session()

    def save(self, session: Session, filename: str):
        with open(filename, 'w+') as f:
            f.write(session.to_json(indent=2))

    def load(self, filename: str) -> Session:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Session file {filename} does not exist")

        with open(filename, 'r+') as f:
            return Session.from_json(f.read())
