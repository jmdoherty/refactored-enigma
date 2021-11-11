# refactored-enigma
A fastapi app for throwing load at, using a redis back end
Runs under uvicorn, listening on port 8000 by default
Borrowing heavily from: https://github.com/shevron/python-redis-demo-counter

Uses environment variables of REDIS_HOST and REDIS_PORT for Redis backend
Assumes localhost:6379 if not set

## Routes:
GET /_name_ - Return value of key *name*
POST /_name_ - Increment value of key *name* by 1 and return that value

### Optional Query Parameters or Path to increase resource usage to service a request
  * method - One of error, loop, memory, sleep 
  * number - An integer used by method
  * http://localhost:8000/somevalue?method=sleep&number=1000 is treated same as http://localhost:8000/somevalue/sleep/100

### Methods:
* error - 1 in _number_ chancee it generates a 418 error
* loop - Loops 1M x _number_ times before completing request
* memory - Create a _number_ MB string in memory before it does so, in increments of 1MB before completing request
* slow - Randomally sleeps for up to _number_ ms before completing the request

## Sample load generation

### Using Curl
Get the value of _somevalue_
>curl -X GET 'http://localhost:8000/somevalue'

Increase the value of _somevalue_ by 1, use the sleep method to sleep up 1000ms
>curl -X POST 'http://localhost:8000/somevalue?method=sleep&number=1000'


### Using wget <br>
Get the value of _somevalue_, looping 5M times before returning
>wget 'http://localhost:8000/somevalue?method=loop&number=5'

Get the value of _somevalue_, sleeping up to 5000ms before returning
* -q : Quiet
* -O- : Write response to STDOUT instead of file
>wget -qO- --post-data '' 'http://localhost:8000/_somevalue_?method=sleep&number=5000'


### Using [Apache Bench](https://httpd.apache.org/docs/2.4/programs/ab.html)
Make a 100 requests to get the value of _somevalue_ at a concurrency of 20
Using the error method to get an error 1:5 times
>ab -n 100 -c 20 http://127.0.0.1:8000/_somevalue_\?method\=error\&number\=5

Make a 100 requests to increment the value of _somevalue_ at a concurrency of 20
Using the sleep method to have each request sleep for up to 100ms
* -n : Number of requests
* -c : Concurrency
* -l : Don't count the fact that the response length changes as an error
* -p : File containing data to POST, can set to /dev/null and just use the url path but still need it to POST
* -T : Content-type for post
>ab -n 100 -c 20 -l -p /dev/null -T application/x-www-form-urlencoded http://127.0.0.1:8000/somevalue/sleep/100

### Using [Siege](https://www.joedog.org/siege-home/)
Siege the server, sending as many requests as possible, incrementing the value of _somevalue_ but getting an error 1 in 10 times
>siege 'http://localhost:8000/what?method=error&number=10 POST'

