from dataclasses import dataclass


@dataclass
class Validations:

    data: dict

    def validateRegister(self):
        if not all(self.data['username'], self.data['email'], self.data['password']):
            return False

        return True
