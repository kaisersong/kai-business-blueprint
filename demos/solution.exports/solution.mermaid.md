---
title: 业务能力蓝图
---
graph TD
    cap-store-ops["门店运营"]
    cap-membership["会员运营"]
    cap-order["订单管理"]
    sys-crm["CRM"]
    sys-crm --> cap-membership
    sys-crm --> cap-order
    sys-pos["POS"]
    sys-pos --> cap-order
    sys-erp["ERP"]
    sys-erp --> cap-store-ops

---
title: 泳道流程图
---
    subgraph actor-store-guide["门店导购"]
        flow-membership-register["会员注册"]
        flow-points-accrual["积分累计"]
    end
    subgraph actor-service["客服"]
        flow-service-followup["售后跟进"]
    end
    flow-membership-register --> flow-points-accrual
    flow-points-accrual --> flow-service-followup

---
title: 应用架构图
---
graph TD
    sys-crm["CRM"]
    sys-pos["POS"]
    sys-erp["ERP"]
    cap-store-ops["门店运营"]
    cap-membership["会员运营"]
    cap-order["订单管理"]
    sys-crm --> cap-membership
    sys-crm --> cap-order
    sys-pos --> cap-order
    sys-erp --> cap-store-ops
