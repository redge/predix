import redis
import json
import os


class RedisManager:
    def __init__(self, redis_name=None):
        vcap_str = os.getenv('VCAP_SERVICES')
        self.redis_name = redis_name
        self.POOL = None
        if vcap_str and self.redis_name:
            self.vcap = json.loads(str(vcap_str))
            if self.vcap['redis-2']:
                for r in self.vcap['redis-2']:
                    if r['name'] == self.redis_name:
                        self.host = r['credentials']['host']
                        self.port = r['credentials']['port']
                        self.password = r['credentials']['password']
                        self.POOL = redis.ConnectionPool(host=self.host, port=self.port, db=0, password=self.password)
                        break

    def getVar(self, var_name):
        if not self.POOL:
            return ''
        svr = redis.Redis(connection_pool=self.POOL)
        response = svr.get(var_name)
        return response

    def setVar(self, var_name, value):
        if self.POOL:
            svr = redis.Redis(connection_pool=self.POOL)
            svr.set(var_name, value)


    def main():
        pass
        #print 'connecting to cf redis'
        #try:
        #    print getVar('test')
        #except redis.exceptions.ConnectionError:
        #    print 'connection error'



if __name__ == '__main__':
    main()

