-- PostgreSQL schema for AI Video Studio MVP.
-- SQLAlchemy can also create these tables automatically with scripts/init_db.py.

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    genre VARCHAR(120) NULL,
    visual_style VARCHAR(120) NOT NULL DEFAULT 'điện ảnh chân thực',
    aspect_ratio VARCHAR(20) NOT NULL DEFAULT '16:9',
    language VARCHAR(60) NOT NULL DEFAULT 'Tiếng Việt',
    default_duration_per_scene INTEGER NOT NULL DEFAULT 8,
    provider_name VARCHAR(80) NOT NULL DEFAULT 'mock_veo',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(120) NULL,
    age VARCHAR(60) NULL,
    gender VARCHAR(60) NULL,
    appearance TEXT NULL,
    face_description TEXT NULL,
    hair_description TEXT NULL,
    outfit_description TEXT NULL,
    dominant_colors VARCHAR(255) NULL,
    personality TEXT NULL,
    voice_description TEXT NULL,
    reference_image_path TEXT NULL,
    fixed_character_prompt TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS episodes (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    episode_number INTEGER NOT NULL DEFAULT 1,
    title VARCHAR(255) NOT NULL,
    script_text TEXT NOT NULL DEFAULT '',
    status VARCHAR(60) NOT NULL DEFAULT 'draft',
    final_video_path TEXT NULL,
    duration_seconds INTEGER NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS scenes (
    id SERIAL PRIMARY KEY,
    episode_id INTEGER NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
    scene_number INTEGER NOT NULL DEFAULT 1,
    title VARCHAR(255) NULL,
    scene_text TEXT NOT NULL DEFAULT '',
    characters_json JSONB NULL,
    location TEXT NULL,
    action TEXT NULL,
    emotion TEXT NULL,
    camera TEXT NULL,
    lighting TEXT NULL,
    sound TEXT NULL,
    dialogue TEXT NULL,
    duration_seconds INTEGER NOT NULL DEFAULT 8,
    video_prompt TEXT NULL,
    negative_prompt TEXT NULL,
    continuity_notes TEXT NULL,
    status VARCHAR(60) NOT NULL DEFAULT 'draft',
    video_job_id VARCHAR(255) NULL,
    video_path TEXT NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS video_jobs (
    id SERIAL PRIMARY KEY,
    scene_id INTEGER NOT NULL REFERENCES scenes(id) ON DELETE CASCADE,
    provider VARCHAR(80) NOT NULL DEFAULT 'mock_veo',
    provider_job_id VARCHAR(255) NULL,
    status VARCHAR(60) NOT NULL DEFAULT 'queued',
    request_payload JSONB NULL,
    response_payload JSONB NULL,
    result_video_path TEXT NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS project_assets (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    asset_type VARCHAR(80) NOT NULL,
    file_path TEXT NOT NULL,
    description TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS app_settings (
    id SERIAL PRIMARY KEY,
    key VARCHAR(120) UNIQUE NOT NULL,
    value TEXT NULL,
    is_secret INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_characters_project_id ON characters(project_id);
CREATE INDEX IF NOT EXISTS idx_episodes_project_id ON episodes(project_id);
CREATE INDEX IF NOT EXISTS idx_scenes_episode_id ON scenes(episode_id);
CREATE INDEX IF NOT EXISTS idx_video_jobs_scene_id ON video_jobs(scene_id);
