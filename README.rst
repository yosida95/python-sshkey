python-sshkey
=============

.. image:: https://badge.fury.io/py/sshkey.svg?dummy
   :target: http://badge.fury.io/py/sshkey


About
-----

SSH key management utility

Supported Key Algorithms
~~~~~~~~~~~~~~~~~~~~~~~~

- RSA
- DSA
- ECDSA

Supported Key Formats
~~~~~~~~~~~~~~~~~~~~~

- OpenSSH (marshal / unmarshal)
- SSH2 (`RFC 4716 <https://tools.ietf.org/html/rfc4716>`_) (marshal only)

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3.6+


Install
-------

.. code:: shell

  $ pip install sshkey

Or

.. code:: shell

  $ python setup.py install


Examples
--------


.. code-block:: python3


   >>> from sshkey.public import (
   ...     SSHKeyType,
   ...     from_openssh,
   ... )
   >>>
   >>> key = from_openssh('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4gMyv02ZZ3W4gKz5VyojiEGCWb1M/wOwpA1CrJiBEaIqgghq9PiT7sfjNzRnwnEKiGh0T31YpmxSC+OyEZLylWIlsdwer84MfIGvo1LA+vnljnMxyLpTZCXbK0tWqIlnjeyTzGMBNuPaq6j1b1Zvyhma1FyovZHIjiCQmpSN2Xu8o4Pq1/cgmDF9T1MKZ3zMJoTg1EjCVtl5OmxFsoXytl69Qreiy21X5Nztpr8eSlLj+0RPl9vbj9lg9ljj/wHuHeiUjHFSDz0YD8Hg01wGITkGyoBhawQLlOprjgtZX7P9TWo+1c9ogeACgTkfV5W3+mytRg2AAgIiY0uiOCzzR yosida95')
   >>>
   >>> key.type is SSHKeyType.RSA
   True
   >>>
   >>> key.length
   2048
   >>>
   >>> print(key.fingerprint())
   d8fef487004e3cb50a9188f9a0f267e4
   >>>
   >>> print(key.pretty_finger_print())
   d8:fe:f4:87:00:4e:3c:b5:0a:91:88:f9:a0:f2:67:e4
   >>>
   >>> print(key.to_openssh())
   ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4gMyv02ZZ3W4gKz5VyojiEGCWb1M/wOwpA1CrJiBEaIqgghq9PiT7sfjNzRnwnEKiGh0T31YpmxSC+OyEZLylWIlsdwer84MfIGvo1LA+vnljnMxyLpTZCXbK0tWqIlnjeyTzGMBNuPaq6j1b1Zvyhma1FyovZHIjiCQmpSN2Xu8o4Pq1/cgmDF9T1MKZ3zMJoTg1EjCVtl5OmxFsoXytl69Qreiy21X5Nztpr8eSlLj+0RPl9vbj9lg9ljj/wHuHeiUjHFSDz0YD8Hg01wGITkGyoBhawQLlOprjgtZX7P9TWo+1c9ogeACgTkfV5W3+mytRg2AAgIiY0uiOCzzR yosida95
   >>>
   >>> print(key.to_ssh2())
   ---- BEGIN SSH2 PUBLIC KEY ----
   Comment: "2048-bit RSA, yosida95"
   AAAAB3NzaC1yc2EAAAADAQABAAABAQC4gMyv02ZZ3W4gKz5VyojiEGCWb1M/wOwpA1CrJi
   BEaIqgghq9PiT7sfjNzRnwnEKiGh0T31YpmxSC+OyEZLylWIlsdwer84MfIGvo1LA+vnlj
   nMxyLpTZCXbK0tWqIlnjeyTzGMBNuPaq6j1b1Zvyhma1FyovZHIjiCQmpSN2Xu8o4Pq1/c
   gmDF9T1MKZ3zMJoTg1EjCVtl5OmxFsoXytl69Qreiy21X5Nztpr8eSlLj+0RPl9vbj9lg9
   ljj/wHuHeiUjHFSDz0YD8Hg01wGITkGyoBhawQLlOprjgtZX7P9TWo+1c9ogeACgTkfV5W
   3+mytRg2AAgIiY0uiOCzzR
   ---- END SSH2 PUBLIC KEY ----
   >>>
   >>> type(key)
   <class 'sshkey.public.SSHRSAPublicKey'>
   >>>
   >>> # Following attributes are available only in `SSHRSAPublicKey`
   >>>
   >>> key.exponent
   65537
   >>>
   >>> key.modulus
   23291361542927526870238657678067236666316634620810120720724799104986752124451659237538147602906450056165165321026453613037422557467367017856171302126254302704561406213684511746522521489098611738674943205317768217444134584525624522689946036426068313269096975514451460214534135120728058539927308903627028117754275189409047243801833683615404857777545626661864188152310484892490356842310296868070586920606890495126519733008950333118463353021953838288379618513638818227222090588352593178733827277689594803980347760492947535017886827810037837197078021077627828242222273041463930547575709340614552834704309059536918401465553


License
-------

python-sshkey is licensed under the 3-Clause BSD License. See ./LICENSE.
