-- Migration: Add two_qubit_gate_count column to circuits table
ALTER TABLE circuits ADD COLUMN two_qubit_gate_count INTEGER;
