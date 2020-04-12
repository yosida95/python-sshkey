# -*- coding: utf-8 -*-

import os
import glob

import sshkey.public


cert_dir = os.path.join(os.path.dirname(__file__), 'data')
cert_files = glob.glob(f'{cert_dir}/*.pub')

fingerprint_list = {
    'ssh-dss': '92bd7424756fa410b77eb7c9653c0f01',
    'ecdsa-sha2-nistp384': 'bb838bfbc862add3e8131d7b542a6138',
    'ecdsa-sha2-nistp256': '4016142a6384cc1daf9de00c9f79a99d',
    'ecdsa-sha2-nistp521': 'a905730f9372dabdc72f267bc27038c5',
    'ssh-rsa': 'd8fef487004e3cb50a9188f9a0f267e4',
}


def test_certs():
    for cert_file in cert_files:
        with open(cert_file, 'r') as cert:
            marshaled_pub = cert.read()
        pub = sshkey.public.from_openssh(marshaled_pub)

        assert pub.comment == 'yosida95'
        assert pub.type is not None
        assert pub.length > 0

        assert pub.fingerprint() == fingerprint_list[pub.type.value]
        assert pub.pretty_finger_print().replace(':', '') == \
            fingerprint_list[pub.type.value]
        assert pub.to_openssh().rstrip() == marshaled_pub.rstrip()

        with open(cert_file + '.ssh2', 'r') as ssh2_cert:
            ssh2_pub = ssh2_cert.read()
        assert pub.to_ssh2().rstrip() == ssh2_pub.rstrip()
