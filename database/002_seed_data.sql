-- Seed data for Kandy AI

-- Insert default user
INSERT INTO users (name, age, height_cm, weight_kg, level, goal)
VALUES (
    'Karthik',
    20,
    163,
    58.0,
    'beginner',
    'Become an advanced calisthenics athlete'
)
ON CONFLICT DO NOTHING;

-- Insert initial coach memory entries
INSERT INTO coach_memory (user_id, memory_type, key, value, confidence)
SELECT 
    id,
    'progression',
    'current_level',
    '{"push": "beginner", "pull": "beginner", "legs": "beginner", "core": "beginner"}'::jsonb,
    1.0
FROM users
WHERE name = 'Karthik'
ON CONFLICT (user_id, key) DO NOTHING;

-- Insert initial body measurement
INSERT INTO body_measurements (user_id, date, weight_kg)
SELECT 
    id,
    CURRENT_DATE,
    58.0
FROM users
WHERE name = 'Karthik'
ON CONFLICT (user_id, date) DO NOTHING;

-- Insert initial achievements
INSERT INTO achievements (user_id, title, description, category, achieved_date, icon)
SELECT 
    id,
    'Welcome Aboard',
    'Started your calisthenics journey with Kandy AI',
    'consistency',
    CURRENT_DATE,
    '🚀'
FROM users
WHERE name = 'Karthik'
ON CONFLICT (user_id, title) DO NOTHING;
