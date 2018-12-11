import http.client

conn = http.client.HTTPSConnection("api.sportradar.us")

# Weekly Depth Information
conn.request("GET", "/nfl/official/trial/v5/en/seasons/2018/REG/07/depth_charts.json?api_key=h3usjtxj2mfpva5cvcscbrjx")

res = conn.getresponse()
data = res.read()

# Weekly Injury Information
# conn.request("GET", "/nfl/official/trial/v5/en/seasons/2018/REG/07/injuries.json?api_key=h3usjtxj2mfpva5cvcscbrjx")

# res = conn.getresponse()
# data = res.read()

print(data.decode("utf-8"))