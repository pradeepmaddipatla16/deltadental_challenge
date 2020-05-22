'''
# assignment_name : conference room problem
# author : pradeep maddipatla
# date: 05/21/2018
# language : python
# version: 3.8

This conference problem can be achieved by designing an appropriate data structure such that the data model should do the heavy lifiting for us and applying cacluations over that model yields the result

# input_format: input is a stream of list of strings and each string is having embedded data which contains conference room#, number of floors e.t.c.,

input 1 --> list of strings which contain different rooms information

eg: 

  '7.11,8,9:00,9:15,14:30,15:00',
  '8.23,6,10:00,11:00,14:00,15:00'

  In the above example while splitting the first string with respect to ',' delimiter leads to a list of string of numeric elements as follows:

  ['7.11','8','9:00','9:15','14:30','15:00']

  a.The first element in the above list represents a floating number '7.11' -> is defined as 7th floor and room#11
  
  b. The second element in the above list explains the capacity of each conference room

  c. from the subsequent elements starting from 3rd element where the pairs of timeslots which explains the availability of the respective conference room in the corresponding floor, for example the consecutive elements starting from '9:00' onwards where the pairs of slots, so in this case 9:00 - 9:15 is one slot which is available for the room 11 in the 7th floor, and 14:30 - 15:00 is another timeslot for availabilty 

input 2 -->  e.g., '5,7,10:30,11:30'
  The second input explains the requirement of # 5 team members, located on the 8th floor, meeting time 10:30 - 11:30

output --> 8.43


Thought process :

1. First we need to select an appropriate data structure to hold and retrieve data according to subsequent computations, if we design a data model with a nested dictionary with floor.roomnumber as key eg., (7.11) in our case, then that key will uniquely defines/identifies the room information of that from the rest of the rooms

2. Then the next step in the algortihm is to check the capacity of each room with the given requirement, we need a room which accomodates all the memebers of the requirment, if there is a room which doesn't able to accomodate the given required number of people then we can filter it out, thus saving the machine for unnecessary computations over the data...

3. Once we filter the rooms according to the accomodation requirement, we need to pair the timeslots of the data stream...for e.g., consider this example ['7.11','8','9:00','9:15','14:30','15:00'] where the elements from 2nd index onwards are the pairwise timeslots...at particular scenario there is chance of these timeslots can be modified/manipulated, this results in discrepencies,so a tuple is a great choice in python for not to modify the time slots data...and frame these list of tuples for each room as values to the capacity key further which is a value to the key which represents floor.roomnumber ('7.11')in our case... 

4. The following is the dictionary data structure which holds the rooms.txt data as in a nested dictionary format

{'7.11' : {'8':[('9:00','9:15'),('14:30','15:00')]}}

5. next step in the algorithm is to check if there is a timeslot that is available in the rooms data as per the requirement, and if yes we can return the same, if there are multiple timeslots across multiple rooms, over multiple floors, then we can calculate the minimum distance from the floor of the input requirment to the floor where the room available, this can be achieved through one pass...

Time and space complexity:

The time taken for constructing the data model will be O(n)and the single pass to lookup will take another O(n) which in total leads to a O(n)

The space for constructing the cache/ dictionary would be  O(n) and the filtered out computation as per the capapcity of a room would be another O(n) which leads to summation of constant O(n)




'''
import math
def main(rooms,req):
  req_ent = req.split(',')
  
  capac, floor, time_slot  = req_ent[0], int(req_ent[1]), tuple(req_ent[2:])

  buf_dict = {}
  
  for each in rooms:
    entities = each.split(',')
    avail_list = entities[2:]
    buf_dict[entities[0]] = {
      entities[1]:
      [(avail_list[i],avail_list[i+1]) for i in range(0,len(avail_list),2)]
    }
  
  '''
  filter the rooms which are sufficient to accomodate the required meeting and check if there are multiple timeslots available across different floors or across different rooms in that case, then optimize the algorithm to get the room available close to the residing floor, this can be achieved by calculating the distance from each floor to all the floors that has rooms available 
  '''
  list_of_rooms = []

  for each in buf_dict.keys():
    actual_capac = list(buf_dict[each].keys())[0]

    if capac <= actual_capac:
      list_of_rooms.append((each,actual_capac))


  min_dis, min_dis_floor_room = math.inf, 0
  for each in list_of_rooms:
    if time_slot in buf_dict[each[0]][each[1]]:
      current_floor = int(each[0].split('.')[0])
      absolute_distance = abs(floor-current_floor)
      if absolute_distance < min_dis:
        min_dis = absolute_distance
        min_dis_floor_room = each[0]

  return min_dis_floor_room
  
if __name__ == '__main__':
  rooms = [ '7.11,8,9:00,9:15,14:30,15:00',
            '8.23,6,10:00,11:00,14:00,15:00',
            '8.43,7,11:30,12:30,17:00,17:30,10:30,11:30',
            '9.511,9,9:30,10:30,12:00,12:15,15:15,16:15,10:30,11:30',
            '9.527,3,9:00,11:00,14:00,16:00,10:30,11:30',
            '9.547,8,10:30,11:30,13:30,15:30,16:30,17:30']
  req = '5,7,10:30,11:30'
answer = main(rooms,req)
print(answer)

'''
Inorder to test the given code we can leverage pytest module and can write unittest functions by invoking the assert and parameterized functions to do a batch streaming of input across expected vs actual test values
'''
