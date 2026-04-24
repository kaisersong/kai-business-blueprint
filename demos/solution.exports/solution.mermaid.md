%% business-blueprint-skill v0.1.0
flowchart TB
    subgraph Systems["Application Systems"]
        direction LR
        sys-erp["ERP"]
        sys-mes["MES"]
        sys-wms["WMS"]
    end
    subgraph 核心能力["核心能力"]
        direction TB
        subgraph row_核心能力_0[""]
            direction LR
            cap-production-plan["生产计划管理"]
            cap-quality-control["质量管理"]
            cap-warehouse["仓储管理"]
            cap-supply-chain["供应链协同"]
        end
    end
    subgraph Actors["参与者"]
        direction LR
        actor-production-mgr["生产经理"]
        actor-quality-inspector["质检员"]
        actor-warehouse-mgr["仓库管理员"]
        actor-purchasing["采购专员"]
    end
    sys-erp --> cap-production-plan
    sys-erp --> cap-warehouse
    sys-mes --> cap-production-plan
    sys-mes --> cap-quality-control
    sys-wms --> cap-warehouse
    actor-production-mgr --> flow-production-scheduling
    actor-quality-inspector --> flow-incoming-inspection
    actor-warehouse-mgr --> flow-warehouse-inbound
    actor-purchasing --> flow-purchase-request
