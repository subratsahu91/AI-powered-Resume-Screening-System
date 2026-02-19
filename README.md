📄 ATS Resume vs Job Description – RAG-Based AI Matching System

An AI-powered Resume Screening System that uses Retrieval-Augmented Generation (RAG) to compare a candidate’s resume with a job description and evaluate ATS (Applicant Tracking System) compatibility.

The system performs semantic matching, keyword analysis, and generates an intelligent match score along with actionable improvement suggestions.

🚀 Project Overview

Most resumes are rejected by ATS before reaching recruiters. This project improves resume screening using:

Large Language Models (LLMs)

Vector Embeddings

Semantic Similarity Search

RAG Architecture

It goes beyond keyword matching and understands contextual alignment between resumes and job descriptions.

🧠 Architecture (RAG Pipeline)

Upload Documents

Resume (PDF / DOCX)

Job Description (Text / PDF)

Text Extraction

Extract content using PyPDF / Docx parser

Text Chunking

Split text into smaller semantic chunks

Embedding Generation

Convert text into vector embeddings

Vector Database

Store embeddings in FAISS / ChromaDB

Similarity Retrieval

Retrieve relevant resume sections based on job description

LLM Analysis

Generate:

Match Score (0–100%)

Skill Gap Analysis

Missing Keywords

Resume Improvement Suggestions

📊 Features

✅ ATS Match Score

✅ Skill Matching Breakdown

✅ Missing Skill Identification

✅ Keyword Optimization Suggestions

✅ Recruiter-Style Feedback

✅ Semantic Comparison (Not just keyword matching)
