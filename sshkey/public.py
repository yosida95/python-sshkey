# -*- coding: utf-8 -*-

import abc
import base64
import enum
import hashlib
import struct


class SSHKeyType(enum.Enum):
    RSA = 'ssh-rsa'
    DSA = 'ssh-dss'
    ECDSA256 = 'ecdsa-sha2-nistp256'
    ECDSA384 = 'ecdsa-sha2-nistp384'
    ECDSA521 = 'ecdsa-sha2-nistp521'


class SSHPublicKey(metaclass=abc.ABCMeta):

    def __init__(self, comment):
        self.comment = comment

    @abc.abstractproperty
    def type(self):
        return None

    @abc.abstractproperty
    def length(self):
        return 0

    @abc.abstractmethod
    def _to_openssh_content(self):
        return

    def to_openssh(self):
        parts = [self.type.value,
                 base64.b64encode(self._to_openssh_content()).decode('ascii')]
        if self.comment:
            parts.append(self.comment)

        return ' '.join(parts)

    def fingerprint(self):
        return hashlib.md5(self._to_openssh_content()).hexdigest()

    def pretty_finger_print(self):
        fp = self.fingerprint()
        return ':'.join(fp[i:i+2] for i in range(0, len(fp), 2))


class SSHRSAPublicKey(SSHPublicKey):

    def __init__(self, exponent, modulus, comment):
        super().__init__(comment)

        self.exponent = exponent
        self.modulus = modulus

    @property
    def type(self):
        return SSHKeyType.RSA

    @property
    def length(self):
        return self.modulus.bit_length()

    def _to_openssh_content(self):
        content = b''
        content += struct.pack(
            '>lBBBBBBB',
            *((7, ) + tuple(self.type.value.encode('ascii'))))

        length = byte_length(self.exponent)
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, ) + tuple(self.exponent.to_bytes(length, 'big'))))

        length = byte_length(self.modulus) + 1
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, 0) + tuple(self.modulus.to_bytes(length - 1, 'big'))))

        return content

    @classmethod
    def from_openssh(cls, content, comment):
        idx = 0
        parts = []
        while len(content) > idx:
            length = struct.unpack('>l', content[idx:idx+4])[0]
            idx += 4

            parts.append(struct.unpack('>' + 'B' * length,
                                       content[idx:idx+length]))
            idx += length

        if len(parts) != 3:
            raise ValueError()

        algorithm_b, exponent_b, modulus_b = parts

        algorithm = ''.join(map(chr, algorithm_b))
        if algorithm != SSHKeyType.RSA.value:
            raise ValueError()

        exponent = bytes_to_int(exponent_b)

        if modulus_b[0] != 0:
            raise ValueError()
        modulus_b = modulus_b[1:]
        modulus = bytes_to_int(modulus_b)

        return cls(exponent, modulus, comment)


class SSHDSAPublicKey(SSHPublicKey):

    def __init__(self, p, q, g, y, comment):
        super().__init__(comment)
        self.p = p
        self.q = q
        self.g = g
        self.y = y

    @property
    def type(self):
        return SSHKeyType.DSA

    @property
    def length(self):
        return self.p.bit_length()

    def _to_openssh_content(self):
        content = b''
        content += struct.pack(
            '>lBBBBBBB',
            *((7, ) + tuple(self.type.value.encode('ascii'))))

        length = byte_length(self.p) + 1
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, 0) + tuple(self.p.to_bytes(length - 1, 'big'))))

        length = byte_length(self.q) + 1
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, 0) + tuple(self.q.to_bytes(length - 1, 'big'))))

        length = byte_length(self.g)
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, ) + tuple(self.g.to_bytes(length, 'big'))))

        length = byte_length(self.y)
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, ) + tuple(self.y.to_bytes(length, 'big'))))

        return content

    @classmethod
    def from_openssh(cls, content, comment):
        idx = 0
        parts = []
        while len(content) > idx:
            length = struct.unpack('>l', content[idx:idx+4])[0]
            idx += 4

            parts.append(struct.unpack('>' + 'B' * length,
                                       content[idx:idx+length]))
            idx += length

        if len(parts) != 5:
            raise ValueError()

        algorithm_b, p_b, q_b, g_b, y_b = parts

        algorithm = ''.join(map(chr, algorithm_b))
        if algorithm != SSHKeyType.DSA.value:
            raise ValueError()

        if p_b[0] != 0:
            raise ValueError()
        p = bytes_to_int(p_b[1:])

        if q_b[0] != 0:
            raise ValueError()
        q = bytes_to_int(q_b[1:])

        g = bytes_to_int(g_b)
        y = bytes_to_int(y_b)
        return cls(p, q, g, y, comment)


class SSHECDSAPublicKey(SSHPublicKey):

    def __init__(self, curve, public_b, comment):
        super().__init__(comment)
        self.curve = curve
        self.public_b = public_b

    @property
    def type(self):
        algorithm = 'ecdsa-sha2-{curve}'.format(curve=self.curve)
        return SSHKeyType(algorithm)

    @property
    def length(self):
        return int(self.curve[-3:])

    def _to_openssh_content(self):
        content = b''
        length = len(self.type.value)
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, ) + tuple(self.type.value.encode('ascii'))))

        length = len(self.curve)
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, ) + tuple(self.curve.encode('ascii'))))

        length = len(self.public_b)
        content += struct.pack(
            '>l' + 'B' * length,
            *((length, ) + tuple(self.public_b)))
        return content

    @classmethod
    def from_openssh(cls, content, comment):
        idx = 0
        parts = []
        while len(content) > idx:
            length = struct.unpack('>l', content[idx:idx+4])[0]
            idx += 4

            parts.append(struct.unpack('>' + 'B' * length,
                                       content[idx:idx+length]))
            idx += length

        if len(parts) != 3:
            raise ValueError()

        algorithm_b, curve_b, public_b = parts
        algorithm = ''.join(map(chr, algorithm_b))
        if not algorithm.startswith('ecdsa-sha2-'):
            raise ValueError()
        expected_curve = algorithm[11:]

        curve = ''.join(map(chr, curve_b))
        if curve != expected_curve or \
                curve not in ('nistp256', 'nistp384', 'nistp521'):
            raise ValueError()

        return cls(curve, bytes(public_b), comment)


def bytes_to_int(bytes_):
    result = 0

    j = (len(bytes_) - 1) * 8
    for b in bytes_:
        result |= b << j
        j -= 8

    return result


def byte_length(i):
    return (7 + i.bit_length()) // 8


def from_openssh(marshaled):
    parts = marshaled.split()
    if len(parts) < 2 or len(parts) > 3:
        raise ValueError()

    algorithm, content_b64 = map(lambda s: s.strip(), parts[:2])
    comment = ''
    if len(parts) == 3:
        comment = parts[2].strip()

    content = base64.b64decode(content_b64)
    if algorithm == SSHKeyType.RSA.value:
        return SSHRSAPublicKey.from_openssh(content, comment)
    elif algorithm == SSHKeyType.DSA.value:
        return SSHDSAPublicKey.from_openssh(content, comment)
    elif algorithm.startswith('ecdsa-sha2-'):
        return SSHECDSAPublicKey.from_openssh(content, comment)
    else:
        raise ValueError()
