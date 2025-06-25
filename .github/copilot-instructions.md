# Copilot Instructions for TravelPlan Project

## Project Overview

**TravelPlan** is a trip planning application that allows users to organize and participate in travel experiences. The system supports trip creation, participation, activity management, user feedback, and advanced querying capabilities.

---

## Entities and Key Concepts

### User
- Attributes:
  - `first_name`, `last_name`, `email`, `city_of_origin`, `registration_date`
- Capabilities:
  - Create trips as organizers
  - Join trips organized by others
  - Provide feedback (score 1 to 5)

### Trip
- Attributes:
  - `name`, `min_participants`, `max_participants`, `organizer`
- Composed of multiple activities
- Users can participate

### Activity
- Types: `visit`, `meal`, `tour`, `transport`, `overnight_stay`
- Attributes:
  - `name`, `start_time`, `duration`, `price`, `location`, `description`, `ticket_codes[]`
- Activities can be **composite** (group of sub-activities)
- Transport activities must define `departure_location` and `arrival_location`
- Overnight stays are limited to **1 per day per user**

### Location
- Attributes:
  - `address`, `city`, `region`, `country`

---

## Participation and Feedback

- Users can be selectively assigned to specific activities within a trip
- If no users are specified for an activity, all trip participants are assumed to join
- Feedback score: integer in `[1, 5]`
- **User rating (`p`)**:
  - `p = 0` if avg. rating ≤ 3
  - Else, `p = floor(0.1 * num_high_scores)` where high score = rating ≥ 4

---

## Core Functionalities

### For Registered Users
- Create and manage trips with associated activities
- Search for trips by:
  - Destination and date range
  - Most visited cities in a time range
  - Number of trips per region in a country and time range
  - Budget, region(s), timeframe, and minimum organizer score

### For System Administrators
- For a given city, compute number of trips organized **per month** in the **last calendar year**

---

## Modeling Constraints

- Ensure data integrity:
  - Only one overnight stay per user per day
  - Users can be assigned to specific activities within a trip
- Composite activities must reference simpler sub-activities
- Trip activity durations and prices must be consistent with travel times and destinations

---

## Implementation Tips

- Use **Entity-Relationship (ER)** modeling for initial design
- Use **UML Use-Case Diagrams** for functional specification
- Generate relational schema from ER model with appropriate foreign keys and constraints
- Implement logic for advanced queries using SQL with parameters

---

## Notes

- The application will be implemented as a **web system** with a database backend
- Consider modular architecture: `User`, `Trip`, `Activity`, `Location`, `Feedback`, `Statistics`

