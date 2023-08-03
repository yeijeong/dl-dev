import redis
import json
class redis_auto:
    def pub_msg(vale):
        r = redis.Redis(host='localhost',port=6379)
        s = r.pubsub()
        s.subscribe('stork_data')
        r.publish('stork_data', vale) # vale 키값
    
    def pub_setmsg(vale):
       r = redis.Redis(host='34.64.240.96', port=6379, db=0)
       s = r.pubsub()
       s.subscribe('stork_data')
       vale = json.dumps(vale,ensure_ascii=False).encode('utf-8')
       r.set('h',vale)

    def sub_msg():
       r = redis.Redis(host='34.64.240.96', port=6379, db=0)
       # subscribe
       s = r.pubsub()
       s.subscribe('stork_data')
       while True :
         res = s.get_message()
         if res is not None :
           res = res['data']
           return res
         
         
    def sub_getmsg():
       r = redis.Redis(host='34.64.240.96', port=6379, db=0)

       s = r.pubsub()
       s.subscribe('stork_data')
       c = r.get('h').decode('utf-8')

       return c
    
    def pub_setmsg2(value):
    # Connect to the Redis server
      redis_host = '34.64.240.96'
      redis_port = 6379
      r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

      # Convert the data to JSON format
      json_data = json.dumps(value)

      # Get the previous value from Redis
      prev_value = r.get('h')
      if prev_value:
         prev_json_data = json.loads(prev_value)

         # Compare the current data with the previous value
         if json_data == prev_json_data:
               # If the data is the same as the previous value, return without publishing
               print("Data is the same as the previous value. Not publishing.")
               return

      # Publish the new data
      r.publish('stork_data', json_data)

      # Store the current value in Redis
      r.set('h', json_data)