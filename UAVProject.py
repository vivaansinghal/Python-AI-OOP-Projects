from abc import ABC, abstractmethod
from typing import List, Generator


class TelemetryError(Exception):
    """Raised when a UAV reports anomalous telemetry data."""
    pass


# 2. Abstract Base Class & Inheritance
class AerialVehicle(ABC):
    def __init__(self, callsign: str, initial_altitude: float):
        self.callsign = callsign
        self._altitude = initial_altitude # Protected attribute
   
    @abstractmethod
    def update_telemetry(self, altitude_change: float) -> None:
        pass


# 3. Encapsulation, Decorators, and Dunder Methods
class ReconDrone(AerialVehicle):
    # Class attribute
    MAX_ALTITUDE = 15000.0


    def __init__(self, callsign: str, initial_altitude: float, battery_capacity: int):
        super().__init__(callsign, initial_altitude)
        self.__battery = battery_capacity # Private attribute (Encapsulation)
       
    # Property Decorator for controlled access
    @property
    def battery(self) -> int:
        return self.__battery


    @battery.setter
    def battery(self, value: int):
        if value < 0 or value > 100:
            raise ValueError("Battery must be between 0 and 100.")
        self.__battery = value


    def update_telemetry(self, altitude_change: float, battery_drain: int = 1) -> None:
        self._altitude += altitude_change
        self.battery -= battery_drain # Uses the setter
       
        if self._altitude > self.MAX_ALTITUDE:
            raise TelemetryError(f"{self.callsign} exceeded max operational altitude!")


    def __str__(self) -> str:
        return f"Drone {self.callsign} | Alt: {self._altitude}ft | Bat: {self.battery}%"


    def __repr__(self) -> str:
        return f"ReconDrone('{self.callsign}', {self._altitude}, {self.battery})"


class FleetManager:
    def __init__(self):
        self._fleet: List[ReconDrone] = []


    def register_drone(self, drone: ReconDrone) -> None:
        self._fleet.append(drone)


    # 4. Generator (PCAP Concept)
    def active_drones(self) -> Generator[ReconDrone, None, None]:
        """Yields drones that have more than 20% battery."""
        for drone in self._fleet:
            if drone.battery > 20:
                yield drone


# --- Execution ---
if __name__ == "__main__":
    manager = FleetManager()
    manager.register_drone(ReconDrone("ALPHA-1", 5000.0, 80))
    manager.register_drone(ReconDrone("BRAVO-2", 12000.0, 15))


    print("Active Fleet Status:")
    for active_drone in manager.active_drones():
        print(active_drone)
        try:
            active_drone.update_telemetry(altitude_change=4000.0) # Will trigger exception
        except TelemetryError as e:
            print(f"ALERT: {e}")

