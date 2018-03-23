"""
Copyright ArxanFintech Technology Ltd. 2018 All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

                 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest
import mock
import json
import os
import sys
import cryption
from cryption.crypto import sign
ROOT_PATH = os.path.join(
    os.path.dirname(__file__),
    "../"
    )
sys.path.append(ROOT_PATH)
from api.poe import POEClient

class Response(object):
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

class POETest(unittest.TestCase):
    """POE test. """
    def setUp(self):
        pass

    def test_create_succ(self):
        """Test create a POE successfully returned. """
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"payload string"
            }

        url = "http://127.0.0.1:9143"
        apikey = "pWEzB4yMM1518346407"
        secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
        nonce = "nonce"
        did = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        cert_path = "./cert_path"
        create_time = "1517818060"
        payload = {
            "id": did,
            "name": "xxxxx",
            "hash": "xxxxx",
            "parent_id": "xxxxx",
            "owner": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
            "metadata": {
                "address": "xxx",
                "telephone": "xxx",
            },
        }

        sig_cipher = "signed cipher"

        tc = POEClient(url, apikey, cert_path)
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.create({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_create_err(self):
        """Test create a POE with error code. """
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
            }
        url = "http://127.0.0.1:9143"
        apikey = "pWEzB4yMM1518346407"
        secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
        nonce = "nonce"
        did = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        cert_path = "./cert_path"
        create_time = "1517818060"
        payload = {
            "id": did,
            "name": "xxxxx",
            "hash": "xxxxx",
            "parent_id": "xxxxx",
            "owner": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
            "metadata": {
                "address": "xxx",
                "telephone": "xxx",
            },
        }

        sig_cipher = "signed cipher"

        tc = POEClient(url, apikey, cert_path)
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.create({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_create_with_sign_succ(self):
        """Test create POE with ed25519 signed body successfully returned. """
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"payload string"
            }

        url = "http://127.0.0.1"
        apikey = "alice"
        secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
        fromdid = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        cert_path = "./cert_path"
        create_time = "1517818060"
        payload = {
            "id": fromdid,
            "name": "xxxxx",
            "hash": "xxxxx",
            "parent_id": "xxxxx",
            "owner": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
            "metadata": {
                "address": "xxx",
                "telephone": "xxx",
            },
        }

        sig_cipher = "signed cipher"

        tc = POEClient(url, apikey, cert_path)
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_post = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.post', mock_do_post):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                _, resp = tc.create_with_sign({}, fromdid, create_time, secret_key_b64, payload)
                self.assertEqual(resp["ErrCode"], 0)

    def test_update_succ(self):
        """Test update poe successfully returned. """
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"payload string"
            }

        url = "http://127.0.0.1:9143"
        apikey = "pWEzB4yMM1518346407"
        secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
        nonce = "nonce"
        did = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        cert_path = "./cert_path"
        create_time = "1517818060"
        payload = {
            "id": did,
            "name": "xxxxx",
            "hash": "xxxxx",
            "parent_id": "xxxxx",
            "owner": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
            "metadata": {
                "address": "xxx",
                "telephone": "xxx",
            },
        }

        sig_cipher = "signed cipher"

        tc = POEClient(url, apikey, cert_path)
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_put = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.put', mock_do_put):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.update({}, body)
                self.assertEqual(resp["ErrCode"], 0)

    def test_update_err(self):
        """Test update poe with error code. """
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
            }

        url = "http://127.0.0.1:9143"
        apikey = "pWEzB4yMM1518346407"
        secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
        nonce = "nonce"
        did = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        cert_path = "./cert_path"
        create_time = "1517818060"
        payload = {
            "id": did,
            "name": "xxxxx",
            "hash": "xxxxx",
            "parent_id": "xxxxx",
            "owner": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
            "metadata": {
                "address": "xxx",
                "telephone": "xxx",
            },
        }

        sig_cipher = "signed cipher"

        tc = POEClient(url, apikey, cert_path)
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_put = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.put', mock_do_put):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                signature = sign(json.dumps(payload), secret_key_b64, did, nonce)
                body = {
                    "payload": json.dumps(payload),
                    "signature": {
                    	"creator": did,
                    	"created": create_time,	
                    	"nonce": nonce,
                    	"signature_value": signature
                    }
                }
                _, resp = tc.update({}, body)
                self.assertEqual(resp["ErrCode"], 107)

    def test_update_with_sign_succ(self):
        """Test update poe with ed25519 signed body successfully returned. """
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"payload string"
            }

        url = "http://127.0.0.1"
        apikey = "alice"
        secret_key_b64 = "0lxEFzMQhn68vY2F0f+nOwP7kl5zjahjPcfyMAJVmzn0HNQssIIYh+c2CgCKEHeUvxqCu6W/sJKqKt2DLJnKpw=="
        fromdid = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        cert_path = "./cert_path"
        create_time = "1517818060"
        payload = {
            "id": fromdid,
            "name": "xxxxx",
            "hash": "xxxxx",
            "parent_id": "xxxxx",
            "owner": "did:axn:8uQhQMGzWxR8vw5P3UWH1j",
            "metadata": {
                "address": "xxx",
                "telephone": "xxx",
            },
        }

        sig_cipher = "signed cipher"

        tc = POEClient(url, apikey, cert_path)
        client_cipher = "client cipher"
        server_cipher = "server cipher"
        mock_do_put = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(side_effect=[sig_cipher, client_cipher, json.dumps(response)])

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.put', mock_do_put):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                _, resp = tc.update_with_sign({}, fromdid, create_time, secret_key_b64, payload)
                self.assertEqual(resp["ErrCode"], 0)

    def test_query_succ(self):
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"payload string"
            }
        fromdid = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        server_cipher = "server cipher"
        mock_do_get = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                _, resp = tc.query({}, fromdid)
                self.assertEqual(resp["ErrCode"], 0)

    def test_query_err(self):
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
            }
        fromdid = "did:ara:8uQhQMGzWxR8vw5P3UWH1j"
        server_cipher = "server cipher"
        mock_do_get = mock.Mock(return_value=Response(200, server_cipher))
        mock_run_cmd = mock.Mock(return_value=json.dumps(response))

        with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
            with mock.patch('requests.get', mock_do_get):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                _, resp = tc.query({}, fromdid)
                self.assertEqual(resp["ErrCode"], 107)

    def test_upload_succ(self):
        response = {
            "ErrCode":0,
            "ErrMessage":"",
            "Method":"",
            "Payload":"payload string"
            }
        
        server_cipher = "server cipher"
        mock_send = mock.Mock(return_value=Response(200, response))
        mock_run_cmd = mock.Mock(side_effect=[server_cipher, json.dumps(response)])

        with mock.patch('requests.Session.send', mock_send):
            with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                file_ = "{}/requirements.txt".format(os.getcwd())
                poeid = "poe id"
                _, resp = tc.upload({}, file_, poeid)
                self.assertEqual(resp["ErrCode"], 0)

    def test_upload_err(self):
        response = {
            "Method":"",
            "ErrCode":107,
            "ErrMessage":"illegal base64 data at input byte 8",
            "Payload":None
            }
        
        server_cipher = "server cipher"
        mock_send = mock.Mock(return_value=Response(200, response))
        mock_run_cmd = mock.Mock(side_effect=[server_cipher, json.dumps(response)])

        with mock.patch('requests.Session.send', mock_send):
            with mock.patch('cryption.crypto.run_cmd', mock_run_cmd):
                tc = POEClient("http://127.0.0.1:9143", "pWEzB4yMM1518346407", "")
                file_ = "{}/requirements.txt".format(os.getcwd())
                poeid = "poe id"
                _, resp = tc.upload({}, file_, poeid)