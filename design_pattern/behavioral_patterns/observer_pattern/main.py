from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

class Status(Enum):
    IDLE = "idle"
    RUNNING = "running"
    FAULT = "fault"

# observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, machine_id: str, status: Status):
        raise NotImplementedError
    
    def subscribe(self, observable: "Observable") -> bool:
        if not isinstance(observable, Observable):
            return False
        observable.register_observer(self)
        return True
    
    def unsubscribe(self, observable: "Observable") -> bool:
        if not isinstance(observable, Observable):
            return False
        observable.remove_observer(self)
        return True
    
# observable interface
@dataclass(kw_only=True)
class Observable(ABC):
    _observers: list[Observer] = field(default_factory=list)

    def register_observer(self, observer: Observer) -> bool:
        if not isinstance(observer, Observer):
            return False 
        self._observers.append(observer)
        return True
    
    def remove_observer(self, observer: Observer) -> bool:
        if observer not in self._observers:
            return False
        self._observers.remove(observer)
        return True
    
    @abstractmethod
    def notify_observers(self):
        raise NotImplementedError

    
# observer class: maintenance engineer
class MaintenanceEngineer(Observer):
    def update(self, machine_id: str, status: Status):
        if status == Status.FAULT:
            print(f"🛠️ [維修部] 收到通知：機台 {machine_id} 發生故障！立即出動。")

# observer class: production dashboard
class ProductionDashboard(Observer):
    def update(self, machine_id: str, status: Status):
        print(f"📺 [看板] 更新狀態：機台 {machine_id} 目前狀態為 [{status.value}]。")

# subject: MES machine
@dataclass(kw_only=True)
class Machine(Observable):
    machine_id: str
    _status: Status = Status.IDLE

    def notify_observers(self) -> None:
        """Notify all the registered observers."""
        for observer in self._observers:
            observer.update(self.machine_id, self._status)

    def set_status(self, status: Status) -> None:
        """Trigger notification when status changed"""
        print(f"\n⚡ 系統訊息：機台 {self.machine_id} 狀態變更為 {status.value}")
        self._status = status
        self.notify_observers()

# simulation
def main():
    # initialise subject
    cnc_machine: Observable = Machine(machine_id="CNC-001")

    # initialise observers
    engineer: Observer = MaintenanceEngineer()
    dashboard: Observer = ProductionDashboard()

    # subscription
    cnc_machine.register_observer(engineer)
    cnc_machine.register_observer(dashboard)

    # simulate all the reactions when machine status changed
    cnc_machine.set_status(Status.RUNNING)
    cnc_machine.set_status(Status.FAULT)


if __name__ == "__main__":
    main()
