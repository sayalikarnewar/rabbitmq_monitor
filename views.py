import aiohttp_jinja2
from pyrabbit.api import Client

#global variable for no. of times of load.
refresh = 0

@aiohttp_jinja2.template("layout.html")
async def monitor(request):
    #data loaded for the first time from the function call
    global refresh
    db = request.app['db']
    await db.collection.drop()
    
    if refresh == 0:
        
        #Client creation
        try:
            client = Client('localhost:15672', 'guest', 'guest')
        except:
            return {"result":"Client not created"}

        #get all the bindings()
        try:
            bindings = client.get_bindings()
            n = len(bindings)
        except:
            return {"result":"binding error"}   

        #final list of all the rows 
        result_list = []
        for i in range(n):
            #dict for storing values for each connection
            try:
                dict_each = {}
                vhost_name = bindings[i]['vhost']
                dict_each['vhost_name'] = vhost_name
                dict_each['exchange_name'] = bindings[i]['source']
                queue_name = bindings[i]['destination']
                dict_each['queue_name'] = queue_name
                dict_each['queue_size'] = client.get_queue_depth(vhost=vhost_name, name=queue_name)  
                result_list.append(dict_each)
            except:
                return {"result" : "data not found"}

        #insert data in the db
        try:
            await db.collection.insert_many(i for i in result_list)

        except:
            return {'result': "data not stored in the db"}
        refresh+=1
        return {'result_list': result_list}       

    #data retrieved from the database after refresh 
    if refresh>0:
        result_list = []
        async for document in db.collection.find():
            result_list.append(document)   
        return {"result_list" : result_list}
