import redis
import json
class redis_auto:
    def pub_msg(vale):
        r = redis.StrictRedis(host='34.64.240.96', port=6379, db=0)
        s = r.pubsub()
        s.subscribe('web_redis')
        r.publish('web_redis', json.dumps(vale)) # vale 키값
      #   print(type(vale))
    
    def pub_setmsg(vale):
       r = redis.StrictRedis(host='34.64.240.96', port=6379, db=0)
       s = r.pubsub()
       s.subscribe('web_redis')
      #  vale = json.dumps(vale,ensure_ascii=False).encode('utf-8')
       r.set('h',json.dumps(vale))

    def sub_msg():
       r = redis.StrictRedis(host='34.64.240.96', port=6379, db=0)
       # subscribe
       s = r.pubsub()
       s.subscribe('web_redis')
      #  while True :
       for message in s.listen():
            # print(type(message))
            if message['type'] == 'message':
                  res_data = message['data']
                  if isinstance(res_data, bytes):
                     res_data = res_data.decode()
                     try:
                        res_dict = json.loads(res_data)
                        return res_dict
                     except json.JSONDecodeError:
                        print(res_data)
                  break
       return None

    def sub_getmsg():
       r = redis.StrictRedis(host='34.64.240.96', port=6379, db=0)

       s = r.pubsub()
       s.subscribe('web_redis')
       c = r.get('h')
       cb = json.loads(c)
       r.delete('h')

       return cb




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
      r.publish('web_redis', json_data)

      # Store the current value in Redis
      r.set('h', json_data)

      
    # def send_data_to_redis(data):
    #      r = redis.StrictRedis(host='34.64.240.96', port=6379, db=0)
         
    #      # 중복값을 제거하고 데이터를 저장하는 방법은 여러 가지가 있습니다.
    #      # 예시로 List 자료형과 Set 자료형을 사용하는 방법을 보여줍니다.

    #      # 1. List 자료형 사용하여 중복값 제거
    #      r.lpush('data_list', data)  # List에 데이터 추가
    #      r.lrem('data_list', 0, data)  # List에서 중복값 제거

    #      # 2. Set 자료형 사용하여 중복값 제거
    #      # r.sadd('data_set', data)  # Set에 데이터 추가

    # def get_list_without_duplicates():
    #      r = redis.StrictRedis(host='34.64.240.96', port=6379, db=0)

    #      # List를 조회하여 중복을 제거하고 반환
    #      unique_values = list(set(r.lrange('data_list', 0, -1)))
    #      return unique_values
