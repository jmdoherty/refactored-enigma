# refactored-enigma
A fastapi app for throwing load at, using a redis back end

Uses environment variables of REDIS_HOST and REDIS_PORT for Redis backend
Assumes localhost:6379 if not set

## Routes: <br>
GET /<name> - Return value of key <name> <br>
POST /<name> - Increment value of key <name> by 1 and return that value <br>

### Optional Query Parameters to increase resource usage to service a request <br>
  * method - One of error, loop, memory, sleep <br>
  * number - An integer used by method <br>

### Methods: <br>
* error - 1 in _number_ chancee it generates a 418 error <br>
* loop - Loops 1M x _number_ times before completing request <br>
* memory - Create a _number_ MB string in memory before it does so, in increments of 1MB before completing request <br>
* slow - Randomally sleeps for up to _number_ ms before completing the request <br>

## Sample load generation <br>

### Using Curl <br>
Get the value of somevalue <br>
curl -X GET 'http://localhost:8000/somevalue' <br>
Increase the value of somevalue by 1, use the sleep method to sleep up 1000ms <br>
curl -X POST 'http://localhost:8000/somevalue?method=sleep&number=1000' <br>

### Using wget <br>
Get the value of blahh, looping 5M times before returning <br>
wget 'http://localhost:8000/blahh?method=loop&number=5' <br>
Get the value of blahh, sleeping up to 5000mss before returning <br>
wget -qO- --post-data '' http://localhost:8000/blahh?method=sleep&number=5000 <br>

### Using Apache Bench <br>
Make a 100 requests to get the value of athing at a concurrency of 20
Using the error method to get an error 1:5 times
ab -n 100 -c 20  http://127.0.0.1:8000/athing\?method\=error\&number\=5
Make a 100 requests to increment the value of athing at a concurrency of 20
Using the sleep method to have each request sleep for up to 100ms
ab -n 100 -c 20 -l -p /dev/null -T application/x-www-form-urlencoded http://127.0.0.1:8000/athing/sleep/100

### Using siege <br>
Siege the server, incrementing the value of what but getting an error 1 in 10 times
siege 'http://localhost:8000/what?method=error&number=10 POST'

