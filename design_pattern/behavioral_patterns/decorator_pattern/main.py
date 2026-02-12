from enum import IntEnum
import functools
import datetime


class UserRole(IntEnum):
    GUEST = 1
    OPERATOR = 2
    ADMIN = 3

# Simulate authorisation check
def require_permission(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user_role = kwargs.get("user_role", "Guest")
            if user_role <= role:
                print(f"⚠️  權限拒絕：角色 {user_role} 無法執行 {func.__name__}")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Simulate ERP synchronisation
def sync_to_erp(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if result:
            print(f"🚀 [ERP 同步] 正在將生產資料 {result['order_id']} 傳送至 ERP 系統...")
            print(f"📅 同步時間：{datetime.datetime.now()}")
        return result
    return wrapper

@require_permission(role=UserRole.OPERATOR)
@sync_to_erp
def report_production(order_id: str, quantity: int, user_role: UserRole):
    """
    MES core: report production
    """
    print(f"✅ [MES 報工] 訂單 {order_id} 已成功生產 {quantity} pcs")
    return {"order_id": order_id, "status": "completed"}

def main():
    print("--- 測試 1：無權限人員嘗試報工 ---")
    report_production("ORD-001", 100, user_role=UserRole.GUEST)

    print("\n--- 測試 2：正式報工並自動同步 ERP ---")
    report_production("ORD-002", 500, user_role=UserRole.ADMIN)

if __name__ == "__main__":
    main()
