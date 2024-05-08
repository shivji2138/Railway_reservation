CREATE DATABASE Railway;
USE Railway;
CREATE TABLE Passengers (
PassengerID INT AUTO_INCREMENT PRIMARY KEY,
Name VARCHAR(100) NOT NULL, 
Age INT,    
Gender CHAR(1),    
Email VARCHAR(100),
Phone INT(20)
);
CREATE TABLE Train (
    TrainID INT AUTO_INCREMENT PRIMARY KEY,
    TrainName VARCHAR(100) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    SourceStation VARCHAR(100) NOT NULL,
    DestinationStation VARCHAR(100) NOT NULL,
    AvailableSeats INT,
    DepartureTime TIME,
    ArrivalTime TIME
);
CREATE TABLE Reservation (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    PassengerID INT,
    TrainID INT,
    JourneyDate DATE,
    SeatNumber VARCHAR(20),
    FOREIGN KEY (PassengerID) REFERENCES Passengers(PassengerID),
    FOREIGN KEY (TrainID) REFERENCES Train(TrainID)
);
CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    ReservationID INT,
    Amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
);
