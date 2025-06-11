# Writing Uber trip data into file
with open("uber_trip.txt", "w") as file:
    file.write("Trip ID: 1001\n")
    file.write("Rider: Naveen\n")
    file.write("Driver: John\n")
    file.write("Fare: $50\n")

# Reading Uber trip data from file
with open("uber_trip.txt", "r") as file:
    data = file.read()
    print(data)

# Appending additional data to file
with open("uber_trip.txt", "a") as file:
    file.write("Trip Completed Successfully.\n")