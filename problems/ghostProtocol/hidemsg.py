from Crypto.Cipher import AES
import base64


class hidemsg(object):
	"""docstring for hidemsg"""
	def __init__(self, secret_key = "dbgkk7%879S87@3dkfnk#V#$@hlkln65"):
		super(hidemsg, self).__init__()
		self.secret_key = secret_key
		self.cipher = AES.new(self.secret_key,AES.MODE_ECB)
	
	def encode(self, msg_text):
		msg_text  = msg_text.rjust(32)
		encoded = base64.b64encode(self.cipher.encrypt(msg_text))
		return encoded

	def decode(self, msg_text):
		decoded = self.cipher.decrypt(base64.b64decode(msg_text))
		return(decoded.strip())
