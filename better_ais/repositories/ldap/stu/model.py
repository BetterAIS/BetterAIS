
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    _state: Optional[str] = None
    attributes: Optional[List[str]] = None
    object_def: Optional[str] = None
    attr_defs: Optional[List[str]] = None
    response: Optional[str] = None
    cursor: Optional[str] = None
    barId: Optional[str] = None
    loginShell: Optional[str] = None
    mendeluRASPassword: Optional[bytes] = None
    mendeluMailDeliveryAddress: Optional[str] = None
    mailLocalAddress: Optional[str] = None
    userPassword: Optional[bytes] = None
    cn: Optional[str] = None
    accountStatus: Optional[str] = None
    gidNumber: Optional[str] = None
    homeDirectory: Optional[str] = None
    sambaPwdLastSet: Optional[str] = None
    mendeluCardChipId: Optional[str] = None
    lastChange: Optional[str] = None
    employeeType: Optional[str] = None
    sambaSID: Optional[str] = None
    objectClass: Optional[str] = None
    uisId: Optional[str] = None
    uidNumber: Optional[str] = None
    host: Optional[str] = None
    mendeluRASCrypt: Optional[bytes] = None
    gecos: Optional[str] = None
    mendeluQuota: Optional[str] = None
    uid: Optional[str] = None
    sn: Optional[str] = None
    givenName: Optional[str] = None
    mail: Optional[str] = None