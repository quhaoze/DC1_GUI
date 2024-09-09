import base64
import pickle


list_1 = [1,1,1]

def change2base64(a):
    serialized_1 = pickle.dumps(a)
    base_64_a = base64.b64encode(serialized_1)
    return base_64_a


def change2original(a):
    receive_data = base64.b64decode(a)
    list_2 = pickle.loads(receive_data)
    return list_2


print(change2original(change2base64(list_1)))
print("-------------------------------")
print(change2base64(list_1))
