-- Kandy AI Database Schema
-- Initial migration for calisthenics workout tracking system

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 1 AND age <= 120),
    height_cm INTEGER NOT NULL CHECK (height_cm >= 50 AND height_cm <= 250),
    weight_kg DECIMAL(5, 2) NOT NULL CHECK (weight_kg >= 20 AND weight_kg <= 300),
    level VARCHAR(50) NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
    goal TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on users for faster lookups
CREATE INDEX idx_users_level ON users(level);

-- Workouts table
CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    day_type VARCHAR(50) NOT NULL CHECK (day_type IN (
        'push', 'pull', 'legs', 'core', 'full_body', 'skill_work', 'active_recovery'
    )),
    greeting TEXT NOT NULL,
    warmup JSONB NOT NULL DEFAULT '{}',
    main_workout JSONB NOT NULL DEFAULT '{}',
    cooldown JSONB NOT NULL DEFAULT '{}',
    daily_habits JSONB NOT NULL DEFAULT '[]',
    notion_page_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT workouts_date_day_unique UNIQUE (date, day_type)
);

-- Create indexes on workouts
CREATE INDEX idx_workouts_date ON workouts(date);
CREATE INDEX idx_workouts_day_type ON workouts(day_type);
CREATE INDEX idx_workouts_notion_page ON workouts(notion_page_id);

-- Workout History table (for tracking completed workouts)
CREATE TABLE workout_history (
    id SERIAL PRIMARY KEY,
    workout_id INTEGER NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
    completed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completion_percentage DECIMAL(5, 2) NOT NULL CHECK (completion_percentage >= 0 AND completion_percentage <= 100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes on workout_history
CREATE INDEX idx_workout_history_workout_id ON workout_history(workout_id);
CREATE INDEX idx_workout_history_completed_at ON workout_history(completed_at);

-- Workout Feedback table
CREATE TABLE workout_feedback (
    id SERIAL PRIMARY KEY,
    workout_id INTEGER NOT NULL REFERENCES workouts(id) ON DELETE CASCADE,
    completion_percentage DECIMAL(5, 2) NOT NULL CHECK (completion_percentage >= 0 AND completion_percentage <= 100),
    rpe INTEGER NOT NULL CHECK (rpe >= 1 AND rpe <= 10),
    pain_level INTEGER NOT NULL CHECK (pain_level >= 0 AND pain_level <= 5),
    recovery_quality VARCHAR(50) NOT NULL CHECK (recovery_quality IN ('poor', 'fair', 'good', 'excellent')),
    sleep_hours DECIMAL(3, 1) NOT NULL CHECK (sleep_hours >= 0 AND sleep_hours <= 24),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT workout_feedback_workout_unique UNIQUE (workout_id)
);

-- Create indexes on workout_feedback
CREATE INDEX idx_workout_feedback_workout_id ON workout_feedback(workout_id);
CREATE INDEX idx_workout_feedback_rpe ON workout_feedback(rpe);
CREATE INDEX idx_workout_feedback_pain_level ON workout_feedback(pain_level);

-- Coach Memory table
CREATE TABLE coach_memory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    memory_type VARCHAR(100) NOT NULL,
    key VARCHAR(255) NOT NULL,
    value JSONB NOT NULL DEFAULT '{}',
    confidence DECIMAL(3, 2) NOT NULL DEFAULT 1.0 CHECK (confidence >= 0 AND confidence <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT coach_memory_user_key_unique UNIQUE (user_id, key)
);

-- Create indexes on coach_memory
CREATE INDEX idx_coach_memory_user_id ON coach_memory(user_id);
CREATE INDEX idx_coach_memory_type ON coach_memory(memory_type);
CREATE INDEX idx_coach_memory_key ON coach_memory(key);

-- Body Measurements table
CREATE TABLE body_measurements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    weight_kg DECIMAL(5, 2) NOT NULL CHECK (weight_kg >= 20 AND weight_kg <= 300),
    body_fat_percentage DECIMAL(5, 2) CHECK (body_fat_percentage >= 0 AND body_fat_percentage <= 100),
    chest_cm DECIMAL(5, 2) CHECK (chest_cm >= 0),
    waist_cm DECIMAL(5, 2) CHECK (waist_cm >= 0),
    arms_cm DECIMAL(5, 2) CHECK (arms_cm >= 0),
    thighs_cm DECIMAL(5, 2) CHECK (thighs_cm >= 0),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT body_measurements_user_date_unique UNIQUE (user_id, date)
);

-- Create indexes on body_measurements
CREATE INDEX idx_body_measurements_user_id ON body_measurements(user_id);
CREATE INDEX idx_body_measurements_date ON body_measurements(date);

-- Personal Records table
CREATE TABLE personal_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exercise_name VARCHAR(255) NOT NULL,
    record_type VARCHAR(100) NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    achieved_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT personal_records_user_exercise_type_unique UNIQUE (user_id, exercise_name, record_type)
);

-- Create indexes on personal_records
CREATE INDEX idx_personal_records_user_id ON personal_records(user_id);
CREATE INDEX idx_personal_records_exercise_name ON personal_records(exercise_name);
CREATE INDEX idx_personal_records_achieved_date ON personal_records(achieved_date);

-- Achievements table
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    achieved_date DATE NOT NULL,
    icon VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT achievements_user_title_unique UNIQUE (user_id, title)
);

-- Create indexes on achievements
CREATE INDEX idx_achievements_user_id ON achievements(user_id);
CREATE INDEX idx_achievements_category ON achievements(category);
CREATE INDEX idx_achievements_achieved_date ON achievements(achieved_date);

-- Trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at on all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workouts_updated_at BEFORE UPDATE ON workouts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workout_history_updated_at BEFORE UPDATE ON workout_history
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workout_feedback_updated_at BEFORE UPDATE ON workout_feedback
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_coach_memory_updated_at BEFORE UPDATE ON coach_memory
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_body_measurements_updated_at BEFORE UPDATE ON body_measurements
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_personal_records_updated_at BEFORE UPDATE ON personal_records
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_achievements_updated_at BEFORE UPDATE ON achievements
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
