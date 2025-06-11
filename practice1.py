
# Uber-Style Python Basics Examples

# List Indexing
rides = ["Airport", "Office", "Mall"]
print("List Indexing:", rides[1])  # Output: Office

# List Slicing
print("List Slicing:", rides[0:2])  # Output: ['Airport', 'Office']

# Tuple Indexing
places = ("Home", "Gym", "Store")
print("Tuple Indexing:", places[0])  # Output: Home

# Tuple Slicing
print("Tuple Slicing:", places[1:])  # Output: ('Gym', 'Store')

# Tuple Reindexing (modifying tuple)
temp = list(places)
temp[0] = "New Home"
places = tuple(temp)
print("Tuple Reindexing:", places)  # Output: ('New Home', 'Gym', 'Store')

# Sorting
fares = [300, 150, 450]
fares.sort()
print("Sorted Fares:", fares)  # Output: [150, 300, 450]

# Set Operations
day1 = {"Ali", "Ravi"}
day2 = {"Ali", "John"}
print("Common Driver:", day1 & day2)  # Output: {'Ali'}

# Lambda Function
fare = lambda km: km * 10
print("Lambda Fare (5 km):", fare(5))  # Output: 50

# filter() Example
ratings = [4.8, 3.9, 5.0]
good = list(filter(lambda r: r > 4.5, ratings))
print("High Ratings:", good)  # Output: [4.8, 5.0]

# map() Example
fares = [100, 200]
tips = list(map(lambda x: x + 20, fares))
print("Fares with Tips:", tips)  # Output: [120, 220]

# reduce() Example
from functools import reduce
fares = [100, 200, 300]
total = reduce(lambda x, y: x + y, fares)
print("Total Fare:", total)  # Output: 600
