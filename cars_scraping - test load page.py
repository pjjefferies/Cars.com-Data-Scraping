
import urllib.request

def get_page(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101'
    headers = {'User-Agent' : user_agent}
    req = urllib.request.Request(url)
    req.add_header('User-Agent', user_agent)
    f = urllib.request.urlopen(req)
    pageFile = f.read().decode('utf-8')
    f.close()
    return pageFile

carPageFile = get_page("http://www.cars.com/vehicledetail/detail/646587428/overview/")

print(carPageFile[0:2000])
