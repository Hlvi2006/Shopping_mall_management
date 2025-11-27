# Technical Documentation

## Architecture
- Modular structure: models (entities), services (business logic), repositories (data access).
- Database: SQLite with tables for shops, rentals, maintenance (relational with foreign keys).
- Design Patterns: Singleton (DB connection), Factory (shop creation).
- OOP/Principles: See code comments for SOLID/GRASP/CUPID applications.

## Class Diagram
(Use a tool like draw.io to visualize; description: Entity (abstract) -> Shop -> SpecialtyShop; Mall uses Repository; Rental and Maintenance compose with Shop via IDs.)

## Relationships
- Composition: Mall has Shops, Rentals, Maintenance.
- Inheritance: SpecialtyShop is-a Shop.
- Association: Rental and Maintenance reference Shop.