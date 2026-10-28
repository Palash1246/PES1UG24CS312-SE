"""Campus shuttle timetable and fleet tracker.

Logs passenger counts per trip, works out average loads, flags under-used
routes and syncs the fleet data to a JSON file.
"""
import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ("Prakash", "Leela", "Imran", "Tom")

def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and append a line to the log list.

    Raises ValueError if the count is not a non-negative whole number and
    KeyError if the route does not exist.
    """
    if isinstance(passenger_count, bool) or not isinstance(passenger_count, int):
        raise ValueError(f"passenger count must be a whole number, got {passenger_count!r}")
    if passenger_count < 0:
        raise ValueError(f"passenger count cannot be negative, got {passenger_count!r}")
    if logs is None:
        logs = []
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs

def remove_route(route_id):
    """Delete a route and its trip history."""
    del routes[route_id]

def average_load(route_id):
    """Return the mean passengers per trip, or None if no trips are logged."""
    trips = routes[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)

def underused_routes():
    """Return ids of routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in routes:
        average = average_load(route_id)
        if average is not None and average < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged

def assign_driver(route_id):
    """Pick a driver for an existing route."""
    if route_id not in routes:
        raise KeyError(route_id)
    return secrets.choice(DRIVERS)

def sync_fleet_data(file="fleet.json"):
    """Write the route data to a JSON file and reload it from disk."""
    with open(file, "w", encoding="utf-8") as out_file:
        json.dump(routes, out_file)
    with open(file, encoding="utf-8") as in_file:
        saved = json.load(in_file)
    routes.clear()
    routes.update(saved)

def main():
    """Run the demo: log sample trips, report stats, look up a route."""
    sample_trips = [("R1", 32), ("R1", 28), ("R2", 4), ("R2", -6), ("R3", "full")]
    logs = []
    for route_id, count in sample_trips:
        try:
            add_trip_log(route_id, count, logs)
        except ValueError as err:
            print("Skipped trip on", route_id, "-", err)
    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ").strip() or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("Unknown route:", choice)
    if "R3" in routes:
        print("R3 average:", average_load("R3"))
    else:
        print("R3 average: route R3 has been removed")

main()
