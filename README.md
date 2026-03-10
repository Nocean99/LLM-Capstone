# LLM Capstone - Music Production Q&A Chatbot

## Overview

This project was my capstone for the **LLMs for IT Professionals** microcredential (StFX University / Digital Nova Scotia). I fine-tuned a large language model using 25 curated query-answer pairs focused on music production topics, creating a specialized Q&A chatbot.

## Key Findings

I compared the fine-tuned model against a pre-trained **Google Gemini** model and discovered:

- **Fine-tuned model**: Performed well on questions within the scope of the training examples, delivering focused and relevant answers about music production
- **Pre-trained Gemini**: Handled broader, out-of-scope questions significantly better due to its extensive training data
- **Takeaway**: This highlighted the importance of comprehensive, large-scale training data in making LLMs versatile -- and why the complex, lengthy, and expensive training processes behind models like Gemini produce such capable general-purpose systems

## Tech Stack

- Python
- LLM Fine-Tuning
- Google Gemini API

## Contents

- `blender/` - Blender scripts and renders for album cover artwork and 3D visualizations
- `study materials/` - Course reference materials covering Python, data analytics, and machine learning