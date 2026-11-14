CREATE SCHEMA IF NOT EXISTS social_empires;
REVOKE ALL ON SCHEMA social_empires FROM PUBLIC;
CREATE TABLE IF NOT EXISTS social_empires.accounts (
    username text PRIMARY KEY CHECK (username=lower(username)),
    password text NOT NULL,
    save_id text NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS social_empires.sessions (
    token_hash text PRIMARY KEY,
    username text NOT NULL REFERENCES social_empires.accounts(username),
    expires bigint NOT NULL
);
CREATE TABLE IF NOT EXISTS social_empires.auth_attempts (
    kind text NOT NULL, address text NOT NULL, attempted bigint NOT NULL
);
CREATE INDEX IF NOT EXISTS auth_attempt_time ON social_empires.auth_attempts(attempted);
CREATE TABLE IF NOT EXISTS social_empires.game_files (
    path text PRIMARY KEY, data jsonb NOT NULL
);
