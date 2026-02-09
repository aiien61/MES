"""
Single Responsibility Principle: 一個類別應該只有一個引起它變化的原因

如果一個類別承擔了太多功能（例如：既處理業務邏輯，又處理資料庫連線，還負責格式化輸出），
那麼當需求變更時（例如資料庫要換、或是輸出格式要改），這個類別就必須被頻繁修改。
這會導致程式碼脆弱、難以測試，且容易產生副作用。

關注點分離 (Separation of Concerns, SoC) : 
SoC 是一個較大、架構層面的方針，而 SRP 則是將這個方針落實到「類別 (Class) 」或「模組 (Module) 」層級的具體規則。
"""
from dataclasses import dataclass
from abc import ABC

class Order(ABC): pass
class Calculator(ABC): pass
class Respository(ABC): pass
class Presenter(ABC): pass

# NOTE  Bad practice: SRP violation
# 單一個類別同時負責資料結構、業務邏輯（計算進度）以及持久化（儲存到資料庫）
@dataclass
class WorkOrderNoSRP(Order):
    order_id: int
    target_qty: int
    completed_qty: int

    # 業務邏輯：計算達成率
    def get_completion_rate(self):
        return (self.completed_qty / self.target_qty) * 100
    
    # 存取邏輯：儲存到資料庫 (引起變化的原因 1)
    def save_to_db(self):
        print(f"Connecting to Database... Saving Order {self.order_id}")

    # 輸出邏輯：格式化報表 (引起變化的原因 2)
    def export_to_json(self):
        import json
        return json.dumps(self.__dict__)
    

# NOTE   Best practice: Following the Single Responsibility Principle (SRP)
# 1. 實體類別：僅負責數據模型
@dataclass
class WorkOrder(Order):
    order_id: int
    target_qty: int
    completed_qty: int

# 2. 邏輯類別：負責生產相關的計算 (業務邏輯)
class WorkOrderCalculator(Calculator):
    @staticmethod
    def calculate_completion_rate(work_order: WorkOrder) -> float:
        return (work_order.completed_qty / work_order.target_qty) * 100
    
# 3. 持久化類別：負責資料庫操作 (Repository 模式)
class WorkOrderRespository(Respository):
    def save(self, work_order: WorkOrder):
        print(f"📦 [DB] 已將工單 {work_order.order_id} 存入資料庫")

# 4. 報表類別：負責格式化輸出 (Presenter 模式)
class WorkOrderPresenter(Presenter):
    @staticmethod
    def to_json(work_order: WorkOrder):
        import json
        return json.dumps(work_order.__dict__, indent=4)

# --- 使用範例 ---
def main():
    order: Order = WorkOrder("PO-2026001", 1_000, 850)
    
    # 計算達成率
    rate: float = WorkOrderCalculator.calculate_completion_rate(order)
    print(f"當前達成率: {rate}%")

    # save
    repo: Respository = WorkOrderRespository()
    repo.save(order)

    # export in JSON format
    print(WorkOrderPresenter.to_json(order))

if __name__ == "__main__":
    main()

"""
Advantages of SRP:
1. High maintainability: 如果未來 MES 需要對接 SAP ERP，只需要修改或新增一個 Repository 類別，
完全不需要動到核心的 WorkOrder 邏輯。

2. Improved testability: 可以針對 WorkOrderCalculator 寫單元測試，而不需要真的啟動資料庫連線。

3. Promote decoupling: 各個組件之間的依賴關係變得清晰。

遵循 SRP 的核心在於：識別並分離那些「會因為不同原因而改變」的代碼。 
在 MES 或 ERP 這種複雜系統中，將「數據」、「邏輯」與「介面/儲存」分離，是保持系統長期穩定運行的關鍵。
"""
