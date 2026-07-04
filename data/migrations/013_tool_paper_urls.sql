-- Migration: Add paper_urls (JSON-encoded array of paper URLs) to tools

ALTER TABLE tools ADD COLUMN paper_urls TEXT;
