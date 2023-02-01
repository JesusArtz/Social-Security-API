from dataclasses import dataclass

@dataclass
class Validations:

    data: dict

    def validateRegister(self):
        if not self.data['username'] or not self.data['email'] or not self.data['password']:
            return False
        return True