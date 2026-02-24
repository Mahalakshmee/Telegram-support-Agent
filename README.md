## 🤖 Telegram Support Agent (Agentic AI + RAG)

Tech Stack: Python, LangChain, Agentic AI, Retrieval-Augmented Generation (RAG), Telegram Bot API, Google APIs

## 📌 Project Overview

The Telegram Support Agent is an AI-powered automation system designed to handle product queries, manage negotiation flows, and assist in closing deals directly through Telegram.

This project leverages:

1.Retrieval-Augmented Generation (RAG)

2.Agentic AI architecture

3.Structured Prompt Engineering

4.Automated Email & Meeting Scheduling Workflows

The primary goal was to build a reliable, controlled AI assistant capable of handling real-world business conversations with minimal hallucination and strict logic enforcement.

## 🛠 Tech Stack

Language: Python

AI Framework: LangChain

Architecture: Agentic AI

Retrieval System: RAG (Retrieval-Augmented Generation)

Messaging Platform: Telegram Bot API

Email Integration: Gmail API

Calendar Integration: Google Calendar API

Automation: Workflow-Based Agent Execution

Data Handling: Vector Retrieval + Structured Logic Control

## 🚀 Key Features

🔎 RAG-based product query handling

💬 Intelligent price negotiation system

📧 Automated email workflow after deal confirmation

📅 AI-powered meeting scheduling agent

🧠 Strict prompt-controlled AI behavior

🛡️ Hallucination minimization using context filtering

## 🧩 System Architecture:

🔹 Module 1: RAG-Based Product & Negotiation Handling

🛍 Product Query Handling

AI responds strictly using RAG-retrieved database context

If product info is unavailable → AI asks for clarification

Casual or unrelated messages → AI ignores product context

Prevents hallucination using strict prompt control

💰 Negotiation Handling (Status-Driven Logic)

Negotiation is controlled using structured status logic:

 ✅ Accepted       - Asks for final confirmation → Triggers email workflow             
 ❌ Rejected       - Politely closes conversation                                      
 ⚠️ Limit Reached - States final price and instructs user to reply only “Yes” or “No” 

 Module 2: Meeting Scheduling Agent (Agentic AI)

This module automatically detects meeting intent.

🗓 Meeting Flow Logic:

If user asks to schedule a meeting → AI enters meeting agent mode

Checks if both date and time are present

If missing → asks only for missing information

If complete → schedules immediately

Understands natural language like:

“tomorrow”

“next Monday”

“this Friday at 4 PM”

These are converted into structured calendar formats automatically.

📧 Automation Workflows

Once a deal is confirmed:

Automated email is triggered

Meeting scheduling workflow is activated

Calendar integration is handled programmatically

## 📸 Screenshots

## 🛍 Product Query via RAG


<img width="895" height="309" alt="Image 1" src="https://github.com/user-attachments/assets/116e507f-a0c7-40ab-a172-a24cf491f38b" />


## 💰 Negotiation Flow


<img width="1241" height="943" alt="Image 3" src="https://github.com/user-attachments/assets/457f1614-bdc7-4428-80eb-ec929ad4c2ee" />


## 📅 Meeting Scheduling Agent


<img width="857" height="577" alt="Image2" src="https://github.com/user-attachments/assets/5a451c8c-53fb-41aa-a2d4-e7b6f7c33b11" />


## 📧 Email Automation Trigger


<img width="1919" height="1022" alt="Image 4" src="https://github.com/user-attachments/assets/e737e632-c81b-4ee0-bd10-fda6168ea37d" />


## 🔐 Security Notice

API credentials and authentication tokens are not included in this repository for security reasons.

To run the project, configure your own Telegram and Google API credentials locally.



