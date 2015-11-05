# Copyright 2015, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Secure client-server interoperability as a unit test."""

import unittest

from grpc.early_adopter import implementations

from grpc_interop import _interop_test_case
from grpc_interop import methods
from grpc_interop import resources

_SERVER_HOST_OVERRIDE = 'foo.test.google.fr'


class SecureInteropTest(
    _interop_test_case.InteropTestCase,
    unittest.TestCase):

  def setUp(self):
    self.server = implementations.server(
        methods.SERVICE_NAME, methods.SERVER_METHODS, 0,
        private_key=resources.private_key(),
        certificate_chain=resources.certificate_chain())
    self.server.start()
    port = self.server.port()
    self.stub = implementations.stub(
        methods.SERVICE_NAME, methods.CLIENT_METHODS, 'localhost', port,
        secure=True, root_certificates=resources.test_root_certificates(),
        server_host_override=_SERVER_HOST_OVERRIDE)

  def tearDown(self):
    self.server.stop()


if __name__ == '__main__':
  unittest.main(verbosity=2)
