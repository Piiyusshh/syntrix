# Syntrix Database Design

## Tables

### users

- id
- full_name
- email
- hashed_password
- is_active
- created_at

---

### organizations

- id
- name
- created_at

---

### documents

- id
- organization_id
- uploaded_by
- filename
- file_type
- file_size
- storage_path
- upload_time

---

### document_chunks

- id
- document_id
- chunk_index
- chunk_text

---

### summaries

- id
- document_id
- summary
- created_at

---

### predictions

- id
- organization_id
- prediction_type
- prediction_result
- created_at

---

### chat_history

- id
- user_id
- question
- answer
- timestamp

---

### activity_logs

- id
- user_id
- action
- timestamp