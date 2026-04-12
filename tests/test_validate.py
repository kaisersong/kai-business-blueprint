from business_blueprint.validate import validate_blueprint


def test_validate_reports_duplicate_ids() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [
                {"id": "cap-order", "name": "Order"},
                {"id": "cap-order", "name": "Order Duplicate"},
            ],
            "flowSteps": [],
            "systems": [],
        },
        "relations": [],
        "views": [],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "DUPLICATE_ID" for issue in result["issues"])


def test_validate_reports_unmapped_first_party_system() -> None:
    blueprint = {
        "version": "1.0",
        "meta": {"revisionId": "r1"},
        "context": {},
        "library": {
            "capabilities": [{"id": "cap-order", "name": "Order"}],
            "flowSteps": [],
            "systems": [
                {
                    "id": "sys-crm",
                    "name": "CRM",
                    "category": "business-app",
                    "supportOnly": False,
                }
            ],
        },
        "relations": [],
        "views": [
            {
                "id": "view-arch",
                "type": "application-architecture",
                "includedNodeIds": ["sys-crm"],
                "includedRelationIds": [],
                "layout": {},
                "annotations": [],
            }
        ],
        "editor": {},
        "artifacts": {},
    }

    result = validate_blueprint(blueprint)

    assert any(issue["errorCode"] == "UNMAPPED_SYSTEM" for issue in result["issues"])
