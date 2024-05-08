
#Daniil Tokarev 
#Student ID: 011389469

import csv
import datetime

with open("Address.csv") as addressCSV:
    addressList = csv.reader(addressCSV)  
    addressList = list(addressList)

with open("Package.csv") as packageCSV:
    packageDetails = csv.reader(packageCSV) 
    packageDetails = list(packageDetails)

with open("Distance.csv") as distanceCSV: 
    distanceList = csv.reader(distanceCSV)
    distanceList = list(distanceList)



class PackageHashTable: #Used hash table from supplemental resources
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])
      
    # Inserts a new item into the hash table.
    def insert(self, key, item): #  does both insert and update 
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        # update key if it is already in the bucket
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
            kv[1] = item
            return True
        
        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
 
    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #print(bucket_list)
 
        # search for the key in the bucket list
        for kv in bucket_list:
          #print (key_value)
          if kv[0] == key:
            return kv[1] # value
        return None
 
    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
 
        # remove the item from the bucket list if it is present.
        if key in bucket_list:
           bucket_list.remove(key)

#Creating package class and attributes 
class Package:
    def __init__(self,ID, address, city, state, zip, deadline, weight, notes, deliveryStatus, departure, deliveryTime):
        self.ID = ID
        self.address= address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.deliveryStatus = deliveryStatus
        self.departure = None
        self.deliveryTime = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.notes, self.deliveryStatus, self.departure, self.deliveryTime)

#function to communicate the status of a package depending on the time
    def packageStatus(self, time):
        if self.deliveryTime == None:
            self.deliveryStatus = "Still at the hub"
        elif time < self.departure:
            self.deliveryStatus = "Still at the hub"
        elif time < self.deliveryTime:
            self.deliveryStatus = "On the way to destination"
        else:
            self.deliveryStatus = "Delivered!"


#Creating the truck class and attributes
class Truck: 
    def __init__(self, averageSpeed, departTime, address, mileage, packages):
        
        self.averageSpeed = averageSpeed
        self.departTime = departTime
        self.address = address
        self.mileage = mileage
        self.packages = packages
        

    def __str__(self):
        return "%s, %s, %s,%s,%s,%s,%s" % (self.averageSpeed, self.departTime, self.address, self.mileage, self.packages)
    
#creation of the 3 trucks and their attributes. 
truck1 = Truck(18, datetime.timedelta(hours=8),"4001 South 700 East", 0.0, [1,13,14,15,16,19,20,27,29,30,31,34,37,40])
truck2 = Truck(18, datetime.timedelta(hours=11),"4001 South 700 East", 0.0,  [2,3,4,5,9,18,26,28,32,35,36,38])
truck3 = Truck(18, datetime.timedelta(hours=9, minutes=5), "4001 South 700 East", 0.0,[6,7,8,10,11,12,17,21,22,23,24,25,33,39])


#function to load the package data into the hashtable 
def loadPackageData(file):
    with open(file) as pData:
        pInfo = csv.reader(pData, delimiter=",")
        next (pInfo)
        for package in pInfo: 
            packageID = int(package[0])
            packageStreet = package[1]
            packageCity = package[2]
            packageState = package[3]
            packageZip = package[4]
            packageDeadline = package[5]
            packageWeight = package[6]
            packageNotes = package[7]
            packageStatus = "Still at the hub"
            packageDeparture = None
            packageDelivery = None

            packages = Package(packageID, packageStreet, packageCity, packageState, packageZip, packageDeadline, packageWeight, packageNotes, packageStatus, packageDeparture, packageDelivery)
            packageHashTable.insert(packageID, packages)

#loading csv data into hash table
packageHashTable = PackageHashTable() 

#finds smallest distance to the next address. Returns finds the address and returns the ID. 
def addressLookup(address):
    for row in addressList:
        if address in row[2]:
            return int(row[0])
#finds the distance between two locations        
def distanceBetween(place1, place2):
    distanceBtwn =  distanceList[place1][place2]    
    if distanceBtwn == "":
        distanceBtwn = distanceList[place2][place1]
    return float(distanceBtwn)   

#loads the package data from the package.csv file into the hashtable
loadPackageData("Package.csv")


#nearest neighbor function 
def packageDelivery(truck):
    onTheWay = []
    for packageID in truck.packages: 
        package = packageHashTable.search(packageID)
        onTheWay.append(package)
                        
    truck.packages.clear()

    while len(onTheWay) > 0:
        upcomingAddress = 2000
        upcomingPackage = None
        for package in onTheWay:
            if distanceBetween(addressLookup(truck.address), addressLookup(package.address)) <= upcomingAddress:
                upcomingAddress = distanceBetween(addressLookup(truck.address), addressLookup(package.address))
                upcomingPackage = package
        #appends the next package to list
        truck.packages.append(upcomingPackage.ID)
        #removes the above package from the onTheWay list
        onTheWay.remove(upcomingPackage)
        truck.mileage += upcomingAddress
        truck.address = upcomingPackage.address

        truck.departTime += datetime.timedelta(hours=upcomingAddress/18)
        upcomingPackage.deliveryTime = truck.departTime
        upcomingPackage.departure = truck.departTime

#calling the nearest neighbor function for each truck and making sure the third truck cannot leave before one of the other two gets back 
packageDelivery(truck1)
packageDelivery(truck2)
truck3.departTime = min(truck1.departTime, truck2.departTime)
packageDelivery(truck3)        

#user interface for the terminal        
class Interface: 

    print("This is the Hoff Delivery Service")
    print("The total mileage is currently ")
    print(truck1.mileage + truck2.mileage + truck3.mileage)
       
    text = input("To begin the program, please type the word 'start'.")
    if text == "start": 
        try:
            user = input("Enter a time to check the status of packages. Use the format hh:mm:ss: ")
            (h,m,s) = user.split(":")
            convert_timedelta = datetime.timedelta(hours=int(h), minutes = int(m), seconds = int(s))

            anotherInput = input("To view a single package, please type 'single'. To view all of the packages, please type 'all'. ")

            if anotherInput == "single":
                try:
                    single = input("Please enter the package ID number: ")
                    package = packageHashTable.search(int(single))
                    package.packageStatus(convert_timedelta)
                    print(str(package))
                    print(truck1.mileage + truck2.mileage + truck3.mileage)

                except ValueError:
                    print("Incorrect entry type. Program will shut down")
                    exit()

            elif anotherInput == "all":
                try: 
                    for packageID in range(1,41):
                        package = packageHashTable.search(packageID)
                        package.packageStatus(convert_timedelta)
                        print(str(package))

                except ValueError: 
                        print("Incorrect entry type. Program will shut down")
                        exit()
                else: 
                        exit()
        except ValueError:
                print("Incorrect entry type. Program will shut down")
                exit()
    elif input != "time":
        print("Incorrect entry type. Program will shut down")
        exit()        



