-- Add a new admin (UUID fix)
INSERT INTO "user" (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$rZEGZ6I4Vt6R5jOqHi2E4e.TUmdYmz/JVnZYevxPQxchXUWr6tLzK',  -- hash of the 'admin1234' (bcrypt, cost=12)
    TRUE
);

-- add commodity for amenities with UUIDv4 
INSERT INTO amenity (id, name) VALUES
    ('a5c3e254-2eb5-45a9-a661-3ab59d86e041', 'WiFi'),
    ('519cadde-4428-49c5-9b2e-87e1575d5f80', 'Swimming Pool'),
    ('f26061cd-e3de-41a9-967e-f86c8f2520e5', 'Air Conditioning');
