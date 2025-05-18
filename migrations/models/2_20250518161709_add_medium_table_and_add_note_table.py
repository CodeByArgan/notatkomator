from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "medium" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL UNIQUE,
    "type" VARCHAR(5) NOT NULL,
    "image" VARCHAR(1024),
    "description" VARCHAR(2048) DEFAULT '',
    "is_public" BOOL NOT NULL DEFAULT False,
    "is_removed" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_edit_at" TIMESTAMPTZ,
    "creator_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "medium"."type" IS 'BOOK: book\nMOVIE: movie\nSHOW: show\nGAME: game\nALBUM: album\nCOMIC: comic';
        CREATE TABLE IF NOT EXISTS "note" (
    "id" UUID NOT NULL PRIMARY KEY,
    "score" INT NOT NULL DEFAULT 0,
    "status" VARCHAR(10) NOT NULL DEFAULT 'backlog',
    "note" VARCHAR(1024) DEFAULT '',
    "is_removed" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_edit_at" TIMESTAMPTZ,
    "medium_id" UUID NOT NULL REFERENCES "medium" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "note"."status" IS 'BACKLOG: backlog\nIN_BETWEEN: in_between\nDONE: done';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "medium";
        DROP TABLE IF EXISTS "note";"""
