import threading
import asyncio
import time, yaml
import AnatoleCode.tapo_p110_measurement_pi as p110  # Power consumption monitoring

# Initialize the connection to the power measurement device's api
with open('AnatoleCode/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

my_event = threading.Event()

energy_consumption_sensor = p110.p110_device(config["sensor"]["current"]["username"],
                                                             config["sensor"]["current"]["password"],
                                                             config["sensor"]["current"]["ip"],
                                                             my_event,
                                                             config["sensor"]["current"]["frequency"])

def thread_test(t):
    name="t"+str(t)
    while not my_event.is_set():
        print("t1 working")
        time.sleep(t)

        print(name," stopped working")

def run_asyncio(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)
    loop.close()

async def async_test(energy_consumption_sensor):
    print("Beginning energy recording")
    await energy_consumption_sensor.start('test_file.csv')
time0 = time.time()

my_event.clear()
t1 = threading.Thread(target=thread_test, args=(1))
t2 = threading.Thread(target=thread_test,args=(2))
t3 = threading.Thread(target=thread_test,args=(3))
energy_thread = threading.Thread(target=run_asyncio,args=
                                    (async_test(energy_consumption_sensor)))
t1.start()
t2.start()
t3.start()
energy_thread.start()

while not time.time()-time0<5:
    pass
my_event.set()
t1.join(timeout=5)
t2.join(timeout=5)
t3.join(timeout=5)
energy_thread.join(timeout=5)

