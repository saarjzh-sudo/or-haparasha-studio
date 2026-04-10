-- אור הפרשה Studio — Supabase tables
-- Run in Supabase SQL editor for project pzvmwfexeiruelwiujxn

CREATE TABLE IF NOT EXISTS ohp_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  parsha_name TEXT NOT NULL,
  message_type TEXT NOT NULL DEFAULT 'parsha',
  subject TEXT,
  html_content TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  pdf_url TEXT,
  moreshet_url TEXT,
  dedication TEXT,
  docx_filename TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ohp_chat_messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  message_id UUID REFERENCES ohp_messages(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ohp_send_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  message_id UUID REFERENCES ohp_messages(id) ON DELETE CASCADE,
  send_type TEXT NOT NULL CHECK (send_type IN ('test', 'live')),
  list_ids INTEGER[],
  campaign_id TEXT,
  sent_at TIMESTAMPTZ DEFAULT NOW()
);
