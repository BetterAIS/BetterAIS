"""
MIT License

Copyright (c) 2023 Illia Chaban

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pydantic

from ..model import User
from better_ais.di import core
from ldap3 import Server, Connection, ALL, Entry


class InvalidLoginOrPassword(Exception):
    def __init__(self):
        super().__init__("Invalid login or password")


class Ldap3Auth:
    def authenticate_ldap(self, login, password):
        basedn = core.configuration.ldap_settings.basedn
        attrs = core.configuration.ldap_settings.attrs

        server = Server(core.configuration.ldap_settings.server, get_info=ALL)
        conn = Connection(server, f"uid={login},{basedn}", password)

        try:
            conn.bind()
        except Exception:
            raise InvalidLoginOrPassword()

        conn.search(basedn, f"(uid={login})", attributes=attrs)
        if not conn.entries:
            raise InvalidLoginOrPassword()
        try:
            user_info = self.extract_user_info(conn.entries[0])
        except pydantic.error_wrappers.ValidationError:
            raise InvalidLoginOrPassword()
        
        if not user_info.userPassword:
            raise InvalidLoginOrPassword()

        return user_info

    def extract_user_info(self, ldap_entry: Entry):
        ldap_entry_dict = {
            str(k): str(v) for k, v in ldap_entry.entry_attributes_as_dict.items()
        }
        user_info = User(
            **ldap_entry_dict
        )
        return user_info
