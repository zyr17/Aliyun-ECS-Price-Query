import json
import base64
import requests
import time

request_delay = 0.2 # seconds
request_number_one_time = 30
request_areas = [
    'cn-wulanchabu',
    'cn-huhehaote',
    'cn-shanghai',
    'cn-hangzhou',
    'cn-beijing',
    'cn-qingdao',
]
request_instances = [
    ['ecs.g5.large', '2v8G'],
    ['ecs.c5.large', '2v4G'],
    ['ecs.c6.large', '2v4G'],
    ['ecs.e5.large', '2v4G'],
    ['ecs.ic5.large', '2v2G'],
    ['ecs.g5.xlarge', '2v8G'],
    ['ecs.c5.xlarge', '4v8G'],
    ['ecs.c6.xlarge', '4v8G'],
    ['ecs.ic5.xlarge', '4v4G'],
    ['ecs.gn5-c4g1.xlarge', 'P100, 4v30G'],
    ['ecs.gn6i-c4g1.xlarge', 'T4, 4v15G'],
    ['ecs.gn6e-c12g1.3xlarge', 'V100, 12v92G'],
    ['ecs.gn5i-c2g1.large', 'P4, 2v8G'],
    ['ecs.gn5i-c4g1.xlarge', 'P4, 4v16G'],
    ['ecs.gn6v-c8g1.2xlarge', 'V100, 8v32G'],
]

request_url = 'https://ecs-buy.aliyun.com/api/ecsPrice/describePrice.json?data='
request_json = "{\"orderType\":\"instance-buy\",\"regionId\":\"\",\"commodity\":{\"zoneId\":\"random\",\"instanceType\":\"\",\"ioOptimized\":true,\"imageType\":\"public\",\"systemDisk\":{\"category\":\"cloud_efficiency\",\"size\":20,\"performanceLevel\":null},\"dataDisks\":[],\"amount\":1,\"priceUnit\":\"Hour\",\"period\":1,\"spotStrategy\":\"SpotWithPriceLimit\",\"spotDuration\":1}}"
request_json = "{\"orderType\":\"instance-buy\",\"regionId\":\"\",\"commodity\":{\"zoneId\":\"random\",\"instanceType\":\"\",\"ioOptimized\":true,\"internetChargeType\":\"PayByTraffic\",\"internetMaxBandwidthOut\":0,\"isp\":null,\"systemDisk\":{\"category\":\"cloud_efficiency\",\"size\":20,\"performanceLevel\":null},\"dataDisks\":[],\"amount\":1,\"priceUnit\":\"Hour\",\"period\":1,\"tenancy\":\"default\",\"resourceGroupId\":\"\",\"spotStrategy\":\"SpotWithPriceLimit\",\"spotDuration\":1},\"logAction\":true}"

def make_request_json(area, instance):
    res = json.loads(request_json)
    res['regionId'] = area
    res['commodity']['instanceType'] = instance
    return res

def make_request_jsons(areas, instances):
    res = []
    for area in areas:
        for instance in instances:
            res.append([area, instance, make_request_json(area, instance)])
    return res

def get_response(req_url):
    resp = requests.get(req_url)
    resp = json.loads(resp.text)
    resp = resp['data']['order']['children']
    res = []
    for r in resp:
        if r['successResponse']:
            res.append(r['data']['order']['tradeAmount'])
        else:
            res.append(999)
    return res

def split_and_request(jsons):
    last = 0
    res = []
    while True:
        n = jsons[last:last + request_number_one_time]
        if len(n) == 0:
            break
        url = request_url + base64.b64encode(json.dumps(n).encode()).decode()
        result = get_response(url)
        res += result
        last += request_number_one_time
        time.sleep(request_delay)
    return res

def main():
    areas, instances, jsons = zip(*make_request_jsons(
                                      request_areas,
                                      list(zip(*request_instances))[0]))
    results = split_and_request(jsons)
    summary = {}
    for a, i, j, r in zip(areas, instances, jsons, results):
        if a == 'cn-huhehaote':
            print(a, i, j, r)
        if i not in summary or summary[i][1] > r:
            summary[i] = [a, r]
    format_s = '%%-%ds  %%-%ds  %%-%ds  %%-10.5f' % (
        max(map(lambda x:len(x[0]), request_instances)),
        max(map(lambda x:len(x[1]), request_instances)),
        max(map(lambda x:len(summary[x][0]), summary)),
    )
    for k, friendly in request_instances:
        print(format_s % (k, friendly, *summary[k]))

if __name__ == '__main__':
    main()
