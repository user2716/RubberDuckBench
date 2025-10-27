class MockRequest:

    def __init__(self, host_value, url='https://example.com'):
        self.headers = {'Host': host_value} if host_value else {}
        self.url = url

    def decode_ascii(self):
        if not self.headers.get('Host'):
            return self._r.url

        host = self.headers['Host']
        if not isinstance(host, str) and isinstance(host, bytes):
            host = host.decode('ascii') #Line in question



    def decode_utf8(self):
        if not self.headers.get('Host'):
            return self.url

        host = self.headers['Host']

        if not isinstance(host, str) and isinstance(host, bytes):
            host = host.decode('utf8') #Change suggested in PR


utf8_str = "👋你好".encode('utf-8')
ascii_str = "hello".encode("ascii")

r1 = MockRequest(ascii_str)
r2 = MockRequest(utf8_str)

result = r1.decode_ascii()
print("Decoding ascii with ascii:", result)
result = r1.decode_utf8()
print("Decoding utf8 with ascii:", result)

result = r2.decode_utf8()
print("Decoding utf8 with utf8:", result)

try: 
    print("Decoding utf8 with ascii...")
    result = r2.decode_ascii()
except UnicodeDecodeError as e:
    print("failed with err:", e)

'''
1. UTF-8 supports more than ascii 
2. error occurs when calling decode with non-ascii characters
3. HTTP headers can only contain ASCII characters: https://www.rfc-editor.org/rfc/rfc7230#section-3.2.4
'''

