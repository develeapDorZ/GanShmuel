from os import path
import requests
import json

HOST = "0.0.0.0"
PORT = "8080"
URL = f'http://{HOST}:{PORT}'

def test():
    test_results = []
    
    dirname = path.dirname(__file__)
    filename = path.join(dirname,"tests.json")
    connectionFailed=False
    with open(filename) as f:
        tests = json.load(f)
    count=0
    for test in tests:
        try:
            api = test['api']
            result = test['result']
            reason = test['description']
            parameters = test['parameters']
            response_type = test['response_type']
            request_type = test['request_type']
            res = None
            count += 1
            if connectionFailed:
                test_results.append({"status":"err","reason":f'{reason} failed(Database not connected)'})
            else:

                if request_type == "GET":
                    res = requests.get(f'{URL}/{api}',(None if parameters == "None" else parameters))
                elif request_type == "POST":
                    res = requests.post(f'{URL}/{api}',(None if parameters == "None" else parameters))
                elif request_type == "PUT":
                    res = requests.put(f'{URL}/{api}',(None if parameters == "None" else parameters))
            
                if response_type == "status_code":
                    if res != None and res.status_code == result:
                        test_results.append({"status":"ok","reason":f'{reason} success'})
                    else:
                        test_results.append({"status":"err","reason":f'{reason} failed'})
                        if count == 2:
                            connectionFailed=True
                elif response_type == "body_response":
                    if res != None and res.content.decode("utf-8") == result:
                        test_results.append({"status":"ok","reason":f'{reason} success'})
                    else:
                        test_results.append({"status":"err","reason":f'{reason} failed'})
                        if count == 2:
                            connectionFailed=True
        except:
            test_results.append({"status":"err","reason":f'{reason} failed'})

    print(json.dumps(test_results))
    return 13

if __name__ == "__main__":
    test()