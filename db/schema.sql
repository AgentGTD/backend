/*
 * Database Schema for AgentGTD Application
 * /
/* 
 * Creates a database named 'agentgtd' 
 */
CREATE DATABASE agentgtd;

/*
 * defines the following tables:
 * tasks:
 * - Stores task information
 * - Fields:
 *   - id: Auto-incrementing unique identifier for each task
 *   - text: Task description/content (required, max 255 chars)
 *   - category: Task category with default value 'Next Actions' (max 50 chars)
 */
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  text VARCHAR(255) NOT NULL,
  category VARCHAR(50) DEFAULT 'Next Actions'
);
