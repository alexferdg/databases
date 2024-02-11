# Architecture of a web application designed to perform CRUD operations with MongoDB as the database

```mermaid
  graph LR
    A[Client Application] -- HTTP Request --> B[Web Server]
    B -- Query --> C[MongoDB ]
    C -- Data Response --> B
    B -- HTTP Response --> A

    style A fill:#32f,stroke:#333,stroke-width:1px
    style B fill,stroke:#333,stroke-width:4px
    style C fill:#2a4,stroke:#333,stroke-width:4px
```

