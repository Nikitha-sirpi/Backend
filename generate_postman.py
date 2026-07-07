import json

postman_collection = {
    "info": {
        "name": "FastAPI Products Auth API",
        "description": "Postman collection for the FastAPI API with Authentication and Relationships",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "variable": [
        {
            "key": "base_url",
            "value": "http://127.0.0.1:8000"
        },
        {
            "key": "token",
            "value": ""
        }
    ],
    "auth": {
        "type": "bearer",
        "bearer": [
            {
                "key": "token",
                "value": "{{token}}",
                "type": "string"
            }
        ]
    },
    "item": [
        {
            "name": "Auth",
            "item": [
                {
                    "name": "Register User",
                    "request": {
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n  \"email\": \"testuser@example.com\",\n  \"password\": \"password123\"\n}"
                        },
                        "url": {
                            "raw": "{{base_url}}/auth/register",
                            "host": ["{{base_url}}"],
                            "path": ["auth", "register"]
                        }
                    },
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "pm.test(\"Status is 201 or 400\", function () {",
                                    "    pm.expect(pm.response.code).to.be.oneOf([201, 400]);",
                                    "});"
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Login",
                    "request": {
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/x-www-form-urlencoded"}
                        ],
                        "body": {
                            "mode": "urlencoded",
                            "urlencoded": [
                                {"key": "username", "value": "testuser@example.com", "type": "text"},
                                {"key": "password", "value": "password123", "type": "text"}
                            ]
                        },
                        "url": {
                            "raw": "{{base_url}}/auth/login",
                            "host": ["{{base_url}}"],
                            "path": ["auth", "login"]
                        }
                    },
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "pm.test(\"Status code is 200\", function () {",
                                    "    pm.response.to.have.status(200);",
                                    "});",
                                    "pm.test(\"Store token\", function () {",
                                    "    var jsonData = pm.response.json();",
                                    "    pm.expect(jsonData).to.have.property('access_token');",
                                    "    pm.collectionVariables.set(\"token\", jsonData.access_token);",
                                    "});"
                                ]
                            }
                        }
                    ]
                }
            ]
        },
        {
            "name": "Products",
            "item": [
                {
                    "name": "Create Product",
                    "request": {
                        "method": "POST",
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n  \"name\": \"Auth Product\",\n  \"description\": \"A protected product\",\n  \"price\": 100.0\n}"
                        },
                        "url": {
                            "raw": "{{base_url}}/items",
                            "host": ["{{base_url}}"],
                            "path": ["items"]
                        }
                    },
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "pm.test(\"Status code is 201\", function () {",
                                    "    pm.response.to.have.status(201);",
                                    "});",
                                    "var jsonData = pm.response.json();",
                                    "if(jsonData.id) { pm.collectionVariables.set(\"product_id\", jsonData.id); }"
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Get All Products",
                    "request": {
                        "method": "GET",
                        "url": {
                            "raw": "{{base_url}}/items?skip=0&limit=100",
                            "host": ["{{base_url}}"],
                            "path": ["items"],
                            "query": [{"key": "skip", "value": "0"}, {"key": "limit", "value": "100"}]
                        }
                    }
                },
                {
                    "name": "Get My Products",
                    "request": {
                        "method": "GET",
                        "url": {
                            "raw": "{{base_url}}/users/me/items",
                            "host": ["{{base_url}}"],
                            "path": ["users", "me", "items"]
                        }
                    },
                    "event": [
                        {
                            "listen": "test",
                            "script": {
                                "exec": [
                                    "pm.test(\"Status code is 200\", function () { pm.response.to.have.status(200); });"
                                ]
                            }
                        }
                    ]
                },
                {
                    "name": "Get Product by ID",
                    "request": {
                        "method": "GET",
                        "url": {
                            "raw": "{{base_url}}/items/{{product_id}}",
                            "host": ["{{base_url}}"],
                            "path": ["items", "{{product_id}}"]
                        }
                    }
                },
                {
                    "name": "Update Product",
                    "request": {
                        "method": "PUT",
                        "header": [{"key": "Content-Type", "value": "application/json"}],
                        "body": {
                            "mode": "raw",
                            "raw": "{\n  \"name\": \"Updated Auth Product Name\",\n  \"price\": 120.0\n}"
                        },
                        "url": {
                            "raw": "{{base_url}}/items/{{product_id}}",
                            "host": ["{{base_url}}"],
                            "path": ["items", "{{product_id}}"]
                        }
                    }
                },
                {
                    "name": "Delete Product",
                    "request": {
                        "method": "DELETE",
                        "url": {
                            "raw": "{{base_url}}/items/{{product_id}}",
                            "host": ["{{base_url}}"],
                            "path": ["items", "{{product_id}}"]
                        }
                    }
                }
            ]
        }
    ]
}

with open("postman_collection.json", "w") as f:
    json.dump(postman_collection, f, indent=2)
